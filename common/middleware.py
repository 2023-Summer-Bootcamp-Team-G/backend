class CsrfCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META["HTTP_X_CSRFTOKEN"] = request.COOKIES.get("csrftoken", None)
        return self.get_response(request)
