from django.shortcuts import redirect
from django.contrib import messages

class ProfileReadyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if request.user.is_authenticated:
            if request.user.profile.verified == 1 and path == '/':
                messages.warning(request, 'Please upload your verification documents to complete your profile.')
        return self.get_response(request)