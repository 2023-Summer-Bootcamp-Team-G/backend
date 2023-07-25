def get_user_data(request):
    session_id = request.data.get("session_id")

    user_id = request.session.get("user_id")
    nick_name = request.session.get("nick_name")

    if user_id and nick_name:  # tmp for dev
        return True
        # user_data = {
        #     "session_id": session_id,
        #     "user_id": user_id,
        #     "nick_name": nick_name,
        # }
    elif session_id is not None:
        print(f"Processed through temporary authentication, id: {session_id}")
        return True
    else:
        return False
        # user_data = {
        #     "session_id": session_id,
        #     "user_id": None,
        #     "nick_name": None,
        # }

    # return JsonResponse(user_data)
