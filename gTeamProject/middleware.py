from django.http import JsonResponse
from question.views import get_user_data


class GetUserDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 뷰(LogoutView)가 호출되기 전에 요청을 처리합니다.
        session_id = request.session.session_key
        user_id = request.session.get("user_id")
        nick_name = request.session.get("nick_name")
        print("GetUserDataMiddleware is called.")
        print("sessionID", session_id)
        print("userID", user_id)
        print("nickName", nick_name)

        response = self.get_response(request)

        # 뷰(LogoutView)가 요청을 처리한 후 응답을 처리합니다.
        if request.path == '/api/logout/' and request.method == 'POST':
            # get_user_data 뷰를 호출하여 세션 정보를 받아옵니다.
            user_data_response = get_user_data(request)
            # 기존 응답 데이터와 세션 정보를 병합합니다.
            if isinstance(response, JsonResponse):
                response_data = dict(response.json())
            else:
                response_data = {}
            response_data.update(user_data_response)

            # JsonResponse로 응답을 감싸줍니다.
            return JsonResponse(response_data, status=response.status_code)

        return response
