from celery import shared_task
from .models import Submit

# from .utils import create_submit, create_answer


def create_image(prompt):
    url = "https://exapmle.com/123565645"
    return url


@shared_task
def create_character(submit_id, prompt):
    result_url = create_image(prompt)
    # submit id로 찾아서 업데이트
    submit = Submit.objects.get(id=submit_id)
    submit.result_url = result_url
    submit.save()

    return {"submit_id": submit_id, "keyword": prompt}
