from django.http import HttpResponseRedirect
from django.urls import reverse


class Notlogin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/login/" or request.path == "/register/":
            if '_auth_user_id' in request.session:
                return HttpResponseRedirect("/")

        response = self.get_response(request)
        return response
