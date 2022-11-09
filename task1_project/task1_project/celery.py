from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task1_project.settings')

app = Celery("task1_project")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "my_test_task": {
        "task": "api.tasks.test_task",
        "schedule": timedelta(seconds=30),
    },
    "increase_debt_every_3_hours": {
        "task": "api.tasks.increase_debt",
        "schedule": timedelta(hours=3),
    },
    "decrease_debt_at_6_30": {
        "task": "api.tasks.decrease_debt",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    },
}

app.autodiscover_tasks()
