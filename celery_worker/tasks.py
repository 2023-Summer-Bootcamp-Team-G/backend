import time
import uuid
import redis

# import asyncio
import logging

from .celery import app
from character.models import Submit
from api.api import upload_img_to_s3
from api.imageGenAPI import ImageGenAPI

import os

MAX_CONCURRENT_REQUESTS = 3

redis_client = redis.StrictRedis(host="redis", port=6379, db=2)

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

image_generators = [ImageGenAPI(os.getenv("BING_SESSION_ID"))]

app.conf.update({"worker_concurrency": MAX_CONCURRENT_REQUESTS * len(image_generators)})


def get_round_robin_index():
    cookie_index = redis_client.incr("cookie_index")
    cookie_index %= len(image_generators)
    return cookie_index


def create_image(key, cookie_index, prompt):
    while True:
        current_requests = redis_client.incr(key)
        if current_requests <= MAX_CONCURRENT_REQUESTS:
            redis_client.delete(key + ":lock")  # 락 해제
            print("get request approval " + str(current_requests))
            print("delete lock " + key + ":lock")
            break
        else:
            redis_client.decr(key)
            time.sleep(1)  # await asyncio.sleep(1)

    try:
        # loop = asyncio.get_event_loop()
        # result = loop.run_until_complete(
        #     image_generators[cookie_index].get_images(prompt)
        # )  # 이거 동기로 변경 예정

        # logger.info(result)

        # return result

        return [
            "https://th.bing.com/th/id/OIG.f_qvMMe9vU945B5aU6tE?pid=ImgGn",
            "https://th.bing.com/th/id/OIG.f_qvMMe9vU945B5aU6tE?pid=ImgGn",
            "https://th.bing.com/th/id/OIG.f_qvMMe9vU945B5aU6tE?pid=ImgGn",
            "https://th.bing.com/th/id/OIG.f_qvMMe9vU945B5aU6tE?pid=ImgGn",
        ], None
    except Exception as e:
        raise e
    finally:
        redis_client.decr(key)


@app.task(bind=True)
def create_character(self, submit_id, keywords, duplicate=False):
    # cookie_index, auth_cookie = get_round_robin_key()
    cookie_index = get_round_robin_index()

    key = "concurrent_requests_" + str(cookie_index)

    lock_acquired = False

    time.sleep(0.4)

    try:
        logger.info(keywords)

        prompt = f"{keywords[3]}에서 {keywords[1]}착용하고 {keywords[2]}들고있는 {keywords[5]} 스타일 {keywords[4]} {keywords[0]} 캐릭터"

        logger.info(prompt)

        lock_owner = str(uuid.uuid4())

        while not lock_acquired:
            lock_acquired = redis_client.setnx(key + ":lock", lock_owner)  # 락 설정
            if lock_acquired:
                redis_client.expire(key + ":lock", 32)  # 락의 자동 만료 설정
                print("get lock " + key + ":lock " + lock_owner)
                logger.info("get lock " + key + ":lock " + lock_owner)

        # loop = asyncio.get_event_loop()
        # result_url, _ = loop.run_until_complete(create_image(key, cookie_index, prompt))
        result_url, _ = create_image(key, cookie_index, prompt)

        if duplicate:
            result_url = upload_img_to_s3(result_url[0])

            submit = Submit.objects.get(id=submit_id)
            submit.result_url = result_url
            submit.save()

        return {"result_url": result_url, "submit_id": submit_id, "keyword": keywords}
    except Exception as e:
        self.update_state(state="FAILURE")

        raise ValueError("Some condition is not met. " + str(e))
    finally:
        if redis_client.get(key + ":lock") == lock_owner:
            redis_client.delete(key + ":lock")  # 락 해제
            print("delete lock " + key + ":lock " + lock_owner)
