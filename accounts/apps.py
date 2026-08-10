"""
Republic of Kandhla - Accounts App Configuration
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Accounts & Users'

    def ready(self):
        """Signals register karo jab app load ho."""
        import accounts.signals  # noqa: F401
