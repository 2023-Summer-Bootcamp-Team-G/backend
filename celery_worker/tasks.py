from .celery import app

from api.api import upload_img_to_s3


def create_image(prompt):
    return [
        "https://th.bing.com/th/id/OIG.ctiYxxryky6aReKI63sl?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.vgrm.XjIyXYT_Xkk2jEM?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.M9rr.HWOki6gF4v92ULt?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.L6mTN8sQmnHQHHvUbWOZ?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
    ]


@app.task
def create_character(submit_id, prompt):
    result_url = create_image(prompt)

    upload_img_to_s3("")  # for import test

    return {"result_url": result_url, "submit_id": submit_id, "keyword": prompt}
