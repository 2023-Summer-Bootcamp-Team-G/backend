from celery import shared_task


def create_image(prompt):
    url = [
        "https://exapmle.com/0",
        "https://exapmle.com/1",
        "https://exapmle.com/2",
        "https://exapmle.com/3",
    ]
    return url


@shared_task
def create_character(submit_id, prompt):
    result_url = create_image(prompt)
    return {"result_url": result_url, "submit_id": submit_id, "keyword": prompt}
