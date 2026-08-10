"""
Republic of Kandhla - Accounts Signals
User model ke post-save aur post-delete events handle karo.
- Mohalla population count auto-update
- New user welcome logging
"""

import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    User save hone par actions:
    1. New user create hone par welcome log
    2. Mohalla change hone par population counts update karo
    """
    if created:
        logger.info(
            f"👤 New user registered: {instance.name} ({instance.email}) "
            f"— Role: {instance.get_role_display()}"
        )

        # Agar mohalla set hai toh population count increment karo
        if instance.mohalla:
            _update_mohalla_population(instance.mohalla)


@receiver(pre_save, sender=User)
def handle_user_pre_save(sender, instance, **kwargs):
    """
    User save hone se pehle purana mohalla check karo.
    Agar mohalla change ho raha hai toh old aur new dono ki population update hogi.
    """
    if not instance.pk:
        return  # New user, skip

    try:
        old_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return

    # Mohalla change detect karo
    if old_user.mohalla_id != instance.mohalla_id:
        # Old mohalla ki population decrement
        if old_user.mohalla:
            instance._old_mohalla = old_user.mohalla
        else:
            instance._old_mohalla = None

        # Signal flag set karo — post_save mein use hoga
        instance._mohalla_changed = True
    else:
        instance._mohalla_changed = False


@receiver(post_save, sender=User)
def handle_mohalla_change(sender, instance, created, **kwargs):
    """
    Mohalla change hone par dono mohallas ki population update karo.
    """
    if created:
        return  # New user already handled above

    if getattr(instance, '_mohalla_changed', False):
        # Old mohalla population update
        old_mohalla = getattr(instance, '_old_mohalla', None)
        if old_mohalla:
            _update_mohalla_population(old_mohalla)

        # New mohalla population update
        if instance.mohalla:
            _update_mohalla_population(instance.mohalla)

        logger.info(
            f"📍 User {instance.name} mohalla changed: "
            f"{old_mohalla.name if old_mohalla else 'None'} → "
            f"{instance.mohalla.name if instance.mohalla else 'None'}"
        )


def _update_mohalla_population(mohalla):
    """Mohalla ki active users count sync karo."""
    count = User.objects.filter(
        mohalla=mohalla,
        is_active=True,
    ).count()
    mohalla.population_count = count
    mohalla.save(update_fields=['population_count'])
