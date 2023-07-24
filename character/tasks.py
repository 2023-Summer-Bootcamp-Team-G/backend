from celery import shared_task
from celery_worker.celery import app


@shared_task
def test_task():
    return None


@app.task
def test_task2():
    return None
