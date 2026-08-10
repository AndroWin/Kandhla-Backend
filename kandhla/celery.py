"""
Republic of Kandhla - Celery Application Configuration
Celery + Redis for background tasks:
- Election phase auto-shifts
- Achaar Sanhita (Code of Conduct) enforcement
- Vote queue processing
- Scheduled ban expiry
"""

import os
from celery import Celery

# Django settings module set karo
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kandhla.settings')

app = Celery('kandhla')

# Django settings se Celery config load karo (CELERY_ prefix wale)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Saare registered apps se tasks auto-discover karo
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to verify Celery is working correctly."""
    print(f'Request: {self.request!r}')
