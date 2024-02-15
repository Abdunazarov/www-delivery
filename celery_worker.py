# thirdparty
from celery import Celery
from celery.schedules import crontab

# project
from settings import BROKER_URL

app = Celery("worker", broker=BROKER_URL, include=["celery_tasks.delivery_costs_task"])

app.conf.beat_schedule = {
    "update-delivery-costs-every-5-minutes": {
        "task": "celery_tasks.delivery_costs_task.update_delivery_costs",
        "schedule": crontab(minute="*/5"),
    },
}

app.conf.timezone = "UTC"
