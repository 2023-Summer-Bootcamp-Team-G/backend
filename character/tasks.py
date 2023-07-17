from celery import shared_task


@shared_task
def create_character(poll_id, nick_name, prompt, answers):
    submit_data = create_submit(poll_id, nick_name, prompt)
    submit_id = submit_data["character_id"]
    create_answer(submit_id, prompt, answers)

    return submit_data
