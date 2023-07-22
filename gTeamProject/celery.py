import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gTeamProject.settings")

app = Celery(
    "gTeamProject", backend="redis://redis:6379", brocker="amqp://rabbitmq:5672"
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
