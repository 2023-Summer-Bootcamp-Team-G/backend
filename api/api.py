import time
import uuid
import base64

# import openai
import requests

from datetime import timedelta, datetime
from aws import AWSManager

from botocore.exceptions import ClientError

# from ratelimit import limits, sleep_and_retry

# openai.api_key = AWSManager.get_secret("openai")["api_key"]


s3_client = AWSManager.get_s3_client()
bucket_name = s3_client.list_buckets()["Buckets"][0]["Name"]
expires_in = int(timedelta(days=7).total_seconds())  # URL의 만료 시간 (초 단위)


def upload_img_to_s3(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download the JPEG file from URL: {url}")

        file_key = str(uuid.uuid4()) + ".jpeg"
        s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=response.content)

        url, expiration_time = generate_presigned_url(file_key)
        return url

    except ClientError as e:
        raise Exception(f"Error generating the presigned URL: {str(e)}")
    except Exception as e:
        raise Exception(
            f"Error processing image and generating presigned URL: {str(e)}"
        )


# # @sleep_and_retry
# # @limits(calls=50, period=60)
# def create_image(uuid: str, prompt: str) -> str:
#     # 동기 작업 수행
#     # global __requestTimeList__

#     # dt = time.perf_counter() - __requestTimeList__
#     # if dt < API_REQUEST_LIMIT:
#     #     time.sleep(API_REQUEST_LIMIT - dt)

#     try:
#         start_time = time.time()
#         response = openai.Image.create(
#             prompt=prompt, n=1, size="256x256", response_format="b64_json"
#         )  # user: id of end-user, for detect abuse

#         # for d in response['data']:
#         #     print(d['url'])

#         # __requestTimeList__ = time.perf_counter()

#         image_data = response["data"][0]["b64_json"]
#         decoded_data = base64.b64decode(image_data)

#         s3_client.put_object(Bucket=bucket_name, Key=uuid, Body=decoded_data)

#         # except ClientError as e: # aws 에러처리 추가

#         url, expiration_time = generate_presigned_url(uuid)

#         if not url:
#             return None, None, None, "Error generating presigned URL"

#         end_time = time.time()
#         processing_time = end_time - start_time

#         print("pre-signed URL:", url)

#         return url, processing_time, expiration_time, None

#     except openai.error.OpenAIError as e:
#         error_message = e.error  # str(e.error)
#         print(e.http_status, error_message)

#         return None, None, None, error_message


# @sleep_and_retry
# @limits(calls=5, period=1)  # 임의 지정
def generate_presigned_url(object_name):
    try:
        expiration_time = datetime.utcnow() + timedelta(seconds=expires_in)

        # Pre-signed URL 생성
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
                "ResponseContentType": "image/png",
            },
            ExpiresIn=expires_in,
        )

        return response, expiration_time
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None, None


# class TaskStatus(str, Enum):
#     RUNNING = "running"
#     COMPLETED = "completed"
#     ERROR = "error"


# async def get_task_result(task_id: str):
#     logging.info("get_check_task")

#     # 비동기 작업 결과 확인 (롱 폴링)
#     if task_id not in tasks:
#         raise HTTPException(status_code=404, detail="Task not found")

#     iteration = 0
#     while tasks[task_id]["status"] == TaskStatus.RUNNING and iteration < 5:
#         await asyncio.sleep(0.2)
#         iteration += 1

#     if tasks[task_id]["status"] == TaskStatus.RUNNING:
#         return Response(status_code=202)
#     elif tasks[task_id]["status"] == TaskStatus.COMPLETED:
#         result = tasks[task_id]["result"]
#         processing_time = tasks[task_id]["processing_time"]
#         return {"result": result, "processing_time": processing_time}
#     else:
#         raise HTTPException(status_code=500, detail=tasks[task_id]["error_message"])


# def renew_urls():
#     current_time = datetime.utcnow()
#     expiration_threshold = timedelta(hours=2)

#     expired_urls = collection.find(
#         {"expiration_time": {"$lt": current_time + expiration_threshold}}
#     )

#     for url_data in expired_urls:
#         object_name = url_data["object_name"]

#         url, expiration_time = generate_presigned_url(object_name)
#         if url is not None:
#             collection.update_one(
#                 {"object_name": object_name},
#                 {"$set": {"result": url, "expiration_time": expiration_time}},
#             )
#         else:
#             logging.error("갱신된 사전 서명된 URL 생성 실패")

# # 객체 목록 출력
# response = s3_client.list_objects(Bucket=bucket_name)
# if "Contents" in response:
#     print("Objects in the bucket:")
#     for obj in response["Contents"]:
#         print(obj["Key"])
# else:
#     print("No objects found in the bucket.")

# # 파일 다운로드
# download_path = "./file.txt"
# s3_client.download_file(bucket_name, key, download_path)

# # 파일 삭제
# s3_client.delete_object(Bucket=bucket_name, Key=key)
