import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smoketracker.settings')

app = Celery('smoketracker')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-achievements-daily': {
        'task': 'tracker.tasks.check_all_user_achievements',
        'schedule': crontab(hour=0, minute=5),  # Runs daily at 12:05 AM
    },
}
