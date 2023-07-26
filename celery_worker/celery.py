import os
import django

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gTeamProject.settings")
django.setup()

app = Celery(include=["celery_worker.tasks"])

app.conf.update(
    {
        "broker_url": "amqp://rabbitmq:5672",
        "result_backend": "redis://redis:6379",
        "accept_content": ["json"],
        "task_serializer": "json",
        "result_serializer": "json",
    }
)
__all__ = ["app"]