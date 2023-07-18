from question.models import Poll
from rest_framework.response import Response
from rest_framework import status
from .serializer import (
    SubmitCreateSerializer,
    AnswerPostSerializer,
)
import random

fixed_question_num = 2


def extract_keyword(answer):
    keyword = ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"]
    num = random.randint(0, 4)
    return keyword[num]


def create_image(prompt):
    url = "https://exapmle.com/"
    return url


def create_submit(poll_id, nick_name, prompt):
    result_url = create_image(prompt)

    poll = Poll.objects.get(id=poll_id)
    user_id = poll.user_id

    submit_data = {
        "user_id": user_id,
        "poll_id": poll_id,
        "result_url": result_url,
        "nick_name": nick_name,
    }

    submit_serializer = SubmitCreateSerializer(data=submit_data)
    if submit_serializer.is_valid():
        submit_instance = submit_serializer.save()
    else:
        return Response(submit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    submit_data["character_id"] = submit_instance.id

    # response data 수정
    submit_data.pop("user_id")
    submit_data.pop("poll_id")
    submit_data["keyowrd"] = prompt

    return submit_data


def create_answer(submit_id, prompt, answers):
    for i, answer in enumerate(answers, start=1):
        if i <= fixed_question_num:
            keyword = prompt[i - 1]
        else:
            keyword = answer["answer_text"]

        question_id = answer["question_id"]
        data = {
            "question_id": question_id,
            "submit_id": submit_id,
            "num": i,
            "content": keyword,
        }
        answer_serializer = AnswerPostSerializer(data=data)
        if answer_serializer.is_valid():
            answer_serializer.save()
        else:
            return Response(
                answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
