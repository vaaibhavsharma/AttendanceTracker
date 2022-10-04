import os

from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juitWebkiosk.settings')

app = Celery('juitWebkiosk')
app.conf.beat_schedule = {
    'update-att-at-11-everyday': {
        'task': 'miniWeb.task.automaticScheduled',
        'schedule': crontab(hour=11, minute=0)
    },
    'update-att-at-2-everyday': {
        'task': 'miniWeb.task.automaticScheduled',
        'schedule': crontab(hour=13, minute=0)
    },
    'update-att-at-4-everyday': {
        'task': 'miniWeb.task.automaticScheduled',
        'schedule': crontab(hour=16, minute=0)
    }
}
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')