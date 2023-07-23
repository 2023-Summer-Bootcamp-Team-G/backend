import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gTeamProject.settings")

# app = Celery(
#     "gTeamProject", backend="redis://redis:6379", brocker="amqp://rabbitmq:5672"
# )

app = Celery()

config = {
    # "task_always_eager": True,
    # "timezone": "Asia/Seoul",
    "broker_url": "amqp://rabbitmq:5672",
    "result_backend": "redis://redis:6379",
    "accept_content": ["json"],
    "task_serializer": "json",
    "result_serializer": "json",
}

# config = {
#     # "broker_url": "pyamqp://guest@localhost//",
#     # "result_backend": "redis://localhost",
#     # "task_serializer": "json",
#     # "accept_content": ["json"],
#     # "result_serializer": "json",
#     "task_time_limit": 600,
#     "task_max_retries": 3,
#     "task_retry_delay": 300,
#     "worker_concurrency": 4,
#     "worker_log_color": False,
#     "beat_schedule": {
#         # 주기적인 작업 스케줄링을 설정할 경우 이곳에 작성합니다.
#     },
# }

# 설정 딕셔너리를 Celery 애플리케이션에 적용합니다.
app.conf.update(config)

# app.config_from_object(config)
# app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
