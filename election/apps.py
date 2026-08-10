"""
Republic of Kandhla - Election App Configuration
"""

from django.apps import AppConfig


class ElectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'election'
    verbose_name = 'Election Commission'

    def ready(self):
        """Signals register karo jab app load ho."""
        import election.signals  # noqa: F401
