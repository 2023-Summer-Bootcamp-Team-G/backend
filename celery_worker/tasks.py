from .celery import app
from api.imageGenAPI import ImageGenAPI
from api.api import upload_img_to_s3
from common.aws import AWSManager
from character.models import Submit


def get_ImageCreator_Cookie():
    try:
        bingCookie = AWSManager.get_secret("BingImageCreator")["cookie"]

        return bingCookie
    except Exception as e:
        raise Exception("BingImageCreator API 키를 가져오는 데 실패했습니다.") from e


def create_image(prompt):
    # image_links = None
    # # try:
    # # 이미지 생성 및 저장
    # auth_cookie = get_ImageCreator_Cookie()  # BingImageCreator API 인증에 사용되는 쿠키 값 가져오기
    # image_generator = ImageGenAPI(auth_cookie)
    # image_links = image_generator.get_images(prompt)

    # # except Exception as e:
    # #     print(f"Error: {str(e)}")
    # # # 이미지 생성에 실패한 경우 처리 (e.g., 오류 응답 반환)
    # # return Response({"error": str(e)})

    # # 이미지 생성이 정상적으로 완료된 경우 결과 반환
    # return image_links

    return [
        "https://th.bing.com/th/id/OIG.ctiYxxryky6aReKI63sl?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.vgrm.XjIyXYT_Xkk2jEM?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.M9rr.HWOki6gF4v92ULt?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.L6mTN8sQmnHQHHvUbWOZ?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
    ]  # tmp


@app.task
def create_character(submit_id, prompt, duplicate=False):
    prompt = ", ".join(prompt)
    result_url = create_image(prompt)
    if duplicate:
        result_url = result_url[0]

        final_url = upload_img_to_s3(result_url)

        submit = Submit.objects.get(id=submit_id)
        submit.result_url = final_url
        submit.save()

    return {"result_url": result_url, "submit_id": submit_id, "keyword": prompt}
