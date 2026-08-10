"""
Republic of Kandhla - Election Signals
Election aur Candidate ke post-save events handle karo.
- MohallaChangeRequest freeze on election announcement
- Candidate approval notification logging
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from election.models import Election, Candidate

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Election)
def handle_election_save(sender, instance, created, **kwargs):
    """
    Election save hone par actions:
    1. New election create hone par logging
    2. REQUIREMENTS.md: "All requests freeze automatically when election date is announced"
       — MohallaChangeRequest freeze by Achaar Sanhita check in serializer handles this
    """
    if created:
        target = instance.mohalla.name if instance.mohalla else instance.city.name
        logger.info(
            f"🗳️ NEW ELECTION ANNOUNCED: {instance.get_election_type_display()} "
            f"for {target} — Phase: {instance.get_phase_display()} "
            f"({instance.start_date.strftime('%Y-%m-%d')} to {instance.end_date.strftime('%Y-%m-%d')})"
        )


@receiver(post_save, sender=Candidate)
def handle_candidate_save(sender, instance, created, **kwargs):
    """
    Candidate save hone par:
    1. New nomination logging
    2. Approval status change logging
    """
    if created:
        logger.info(
            f"📋 New nomination: {instance.user.name} in "
            f"{instance.election} (Credibility: {instance.user.credibility_score})"
        )
    else:
        # Approval status change detect karo
        if instance.is_approved and instance.symbol:
            logger.info(
                f"✅ Candidate APPROVED: {instance.user.name} "
                f"— Symbol: {instance.symbol} in {instance.election}"
            )
