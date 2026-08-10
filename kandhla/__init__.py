# Kandhla Django Project Package
# Celery app yahan import hota hai taaki Django start hone par Celery ready ho

from kandhla.celery import app as celery_app

__all__ = ('celery_app',)
