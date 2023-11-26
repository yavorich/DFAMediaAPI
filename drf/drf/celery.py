import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")
app = Celery("drf")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "special_offer": {
        "task": "shop_api.tasks.send_special_offer",
        "schedule": crontab()  # для теста 1 минута
    }
}
