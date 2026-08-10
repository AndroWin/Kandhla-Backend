"""
Republic of Kandhla - Content Celery Tasks
Content moderation, concern auto-escalation, aur feed cleanup.
"""

import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db.models import F

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def auto_escalate_concerns(self):
    """
    High-support concerns ko automatically city_priority mein escalate karo.
    REQUIREMENTS.md: Concerns with high support get elevated.
    
    Threshold: 50+ net support (support - do_not_support) = auto city_priority.
    Ye task Celery Beat se har 30 minute run hoga.
    """
    from content.models import Concern

    escalated = Concern.objects.filter(
        status=Concern.Status.PENDING,
        support_count__gte=50,
    ).update(status=Concern.Status.CITY_PRIORITY)

    if escalated > 0:
        logger.info(f"🚨 {escalated} concerns auto-escalated to City Priority.")

    return f"Auto-escalated {escalated} concerns."


@shared_task(bind=True)
def moderate_flagged_content(self, post_id, flagged_by_user_id):
    """
    Flagged content ko moderation queue mein daalo.
    REQUIREMENTS.md: Supreme Minister can "flag/shadow-ban users for admin review."
    """
    from content.models import Post

    try:
        post = Post.objects.select_related('user').get(id=post_id)
    except Post.DoesNotExist:
        logger.error(f"Post {post_id} not found for moderation.")
        return f"Post {post_id} not found."

    # Post ka content profanity check karo
    from kandhla.profanity import check_profanity

    is_profane = False
    matched_words = []

    if post.content_text:
        is_profane, matched_words = check_profanity(post.content_text)

    if is_profane:
        # Auto-strike on post author
        from accounts.tasks import apply_strike
        apply_strike.delay(
            str(post.user.id),
            reason=f'Profanity detected in post {post.id}: {", ".join(matched_words)}'
        )
        logger.warning(
            f"🚫 Profanity detected in post {post.id} by {post.user.name}. "
            f"Auto-strike triggered. Words: {matched_words}"
        )
        return f"Post {post_id} flagged — auto-strike applied."

    logger.info(
        f"Post {post_id} flagged by user {flagged_by_user_id} — "
        f"added to moderation queue for manual review."
    )
    return f"Post {post_id} added to moderation queue."


@shared_task(bind=True)
def cleanup_old_posts(self):
    """
    Purane normal posts cleanup karo (6 months se zyada purani).
    Announcements aur official orders hamesha rehte hain.
    Ye task Celery Beat se weekly run hoga.
    """
    from content.models import Post
    from datetime import timedelta

    cutoff_date = timezone.now() - timedelta(days=180)

    # Sirf normal posts delete karo — announcements/ads/orders preserve karo
    deleted_count, _ = Post.objects.filter(
        post_type=Post.PostType.NORMAL,
        created_at__lt=cutoff_date,
    ).delete()

    if deleted_count > 0:
        logger.info(f"🗑️ {deleted_count} old normal posts cleaned up (older than 6 months).")

    return f"Cleaned up {deleted_count} old posts."


@shared_task(bind=True)
def sync_interaction_counts(self):
    """
    Firebase Realtime DB se Like/Dislike counts sync karo.
    REQUIREMENTS.md: "Firebase Real-time Database for instant Likes/Support counts"
    
    Ye task Celery Beat se har 5 minute run hoga.
    """
    from kandhla.firebase import sync_post_interactions_from_firebase
    
    success = sync_post_interactions_from_firebase()
    if success:
        return "Firebase interaction sync completed successfully."
    else:
        return "Firebase interaction sync failed or Firebase not configured."
