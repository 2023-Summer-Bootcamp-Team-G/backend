from enum import Enum


class TaskStatus(str, Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"


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
