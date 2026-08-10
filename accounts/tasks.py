"""
Republic of Kandhla - Accounts Celery Tasks
Ban expiry automation aur Credibility Score management.
REQUIREMENTS.md ke mutabiq 3-Strike moderation system:
- 1st Strike: 6-hour Shadow Ban
- 2nd Strike: 24-hour Ban
- 3rd Strike: 3-day Ban (72 hours)
- 4th Strike: Permanent Ban with public "Featured Banned Profile" badge
"""

import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db.models import F

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def check_ban_expiry(self):
    """
    Expired bans automatically lift karo.
    Ye task Celery Beat se har 15 minute run hoga.
    Ban period khatam hone par user ka ban_until field None ho jayega.
    """
    from accounts.models import User

    now = timezone.now()

    # Saare users jinka ban expire ho chuka hai (permanent ban wale nahi)
    expired_bans = User.objects.filter(
        ban_until__isnull=False,
        ban_until__lte=now,
        strike_count__lt=4,  # 4th strike = permanent ban, lift nahi hoga
    )

    count = expired_bans.count()
    if count > 0:
        expired_bans.update(ban_until=None)
        logger.info(f"🔓 {count} user bans expired and lifted.")

    return f"Lifted {count} expired bans."


@shared_task(bind=True)
def apply_strike(self, user_id, reason='Content policy violation'):
    """
    User pe strike lagao aur appropriate ban apply karo.
    REQUIREMENTS.md 3-Strike Rule:
    - 1st Strike: 6-hour Shadow Ban
    - 2nd Strike: 24-hour Ban
    - 3rd Strike: 3-day Ban (72 hours)
    - 4th Strike: Permanent Ban
    """
    from accounts.models import User

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for strike application.")
        return f"User {user_id} not found."

    kandhla_settings = settings.KANDHLA_SETTINGS

    # Strike count increment karo
    user.strike_count = F('strike_count') + 1
    user.save(update_fields=['strike_count'])
    user.refresh_from_db()

    now = timezone.now()
    ban_hours = 0

    if user.strike_count == 1:
        ban_hours = kandhla_settings['STRIKE_1_BAN_HOURS']  # 6 hours
    elif user.strike_count == 2:
        ban_hours = kandhla_settings['STRIKE_2_BAN_HOURS']  # 24 hours
    elif user.strike_count == 3:
        ban_hours = kandhla_settings['STRIKE_3_BAN_HOURS']  # 72 hours
    elif user.strike_count >= 4:
        # Permanent ban — ban_until bahut future mein set karo
        user.ban_until = now.replace(year=now.year + 100)
        user.is_active = False  # Account deactivate
        user.save(update_fields=['ban_until', 'is_active'])

        logger.warning(
            f"⛔ PERMANENT BAN: {user.name} ({user.email}) — "
            f"Strike #{user.strike_count}. Reason: {reason}"
        )
        return f"Permanent ban applied to {user.name}. Strike #{user.strike_count}."

    if ban_hours > 0:
        from datetime import timedelta
        user.ban_until = now + timedelta(hours=ban_hours)
        user.save(update_fields=['ban_until'])

    # Credibility Score penalty
    penalty = kandhla_settings['CREDIBILITY_PENALTY_PER_STRIKE']
    User.objects.filter(id=user_id).update(
        credibility_score=F('credibility_score') - penalty,
    )

    logger.warning(
        f"⚠️ STRIKE #{user.strike_count}: {user.name} ({user.email}) — "
        f"Ban: {ban_hours}h, Credibility -{penalty}. Reason: {reason}"
    )

    return (
        f"Strike #{user.strike_count} applied to {user.name}. "
        f"Ban: {ban_hours} hours. Credibility -{penalty}."
    )


@shared_task(bind=True)
def boost_credibility(self, user_id, points=5, reason='Support received'):
    """
    User ka Credibility Score boost karo.
    REQUIREMENTS.md: "High support increases the author's Credibility Score."
    """
    from accounts.models import User

    try:
        User.objects.filter(id=user_id).update(
            credibility_score=F('credibility_score') + points,
        )
        logger.info(f"Credibility +{points} for user {user_id}. Reason: {reason}")
        return f"Credibility +{points} for user {user_id}."
    except Exception as e:
        logger.error(f"Credibility boost failed for user {user_id}: {e}")
        return f"Failed: {e}"


@shared_task(bind=True)
def update_mohalla_populations(self):
    """
    Saare mohallas ki population count sync karo.
    Active users count = mohalla ki population.
    Ye task Celery Beat se daily run hoga.
    """
    from accounts.models import User
    from ecosystem.models import Mohalla

    updated = 0
    for mohalla in Mohalla.objects.all():
        actual_count = User.objects.filter(
            mohalla=mohalla,
            is_active=True,
        ).count()

        if mohalla.population_count != actual_count:
            mohalla.population_count = actual_count
            mohalla.save(update_fields=['population_count'])
            updated += 1

    if updated > 0:
        logger.info(f"📊 Population count updated for {updated} mohallas.")

    return f"Updated population for {updated} mohallas."
