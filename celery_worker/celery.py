from celery import Celery


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
