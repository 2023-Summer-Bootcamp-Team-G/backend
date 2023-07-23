from celery import shared_task


def create_image(prompt):
    # url = [
    #     "https://exapmle.com/0",
    #     "https://exapmle.com/1",
    #     "https://exapmle.com/2",
    #     "https://exapmle.com/3",
    # ]
    # return url

    url = [
        "https://th.bing.com/th/id/OIG.ctiYxxryky6aReKI63sl?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.vgrm.XjIyXYT_Xkk2jEM?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.M9rr.HWOki6gF4v92ULt?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
        "https://th.bing.com/th/id/OIG.L6mTN8sQmnHQHHvUbWOZ?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
    ]

    return url


@shared_task
def create_character(submit_id, prompt):
    result_url = create_image(prompt)
    return {"result_url": result_url, "submit_id": submit_id, "keyword": prompt}
