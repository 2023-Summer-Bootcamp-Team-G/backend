from django.http import JsonResponse
from rest_framework.views import APIView


class health_check(APIView):
    def get(self, request):
        # 여기에서 서버의 상태를 체크하고, 필요한 정보를 담은 JSON 응답을 작성합니다.
        # 예시로 간단하게 "status"가 "healthy"인 JSON 응답을 반환하겠습니다.
        status_response = {
            'status': 'healthy',
            'details': {
                'disk_space': 'OK',
                'memory': 'OK',
                'database': 'OK'
                # 추가적인 상태 정보가 있다면 이곳에 추가하세요.
            }
        }
        # JSON 형태의 응답을 반환합니다.
        return JsonResponse(status_response)
