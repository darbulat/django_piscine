import random
from django.http import HttpRequest
from d06 import settings


class MyMiddleware:
    SESSION_EXPIRE_TIME = 42
    SESSION_TIMEOUT_KEY = "_session_anonymous_timestamp_"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):

        if not request.user.is_authenticated:
            request.session.clear_expired()
            if request.session.is_empty():
                request.session.set_expiry(self.SESSION_EXPIRE_TIME)
            request.user.username = request.session.setdefault(
                'anonymous',
                random.choice(settings.RANDOM_NAMES)
            )
        else:
            request.session.set_expiry(6000)
        response = self.get_response(request)

        return response
