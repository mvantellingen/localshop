from django.conf import settings
from django.contrib.auth.decorators import login_required


class RequireLoginMiddleware(object):

    def __init__(self):
        self.public_paths = [settings.LOGIN_URL]

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            return None

        if request.path.startswith(settings.STATIC_URL):
            return None

        if request.path in self.public_paths:
            return None

        return login_required(view_func)(request, *view_args, **view_kwargs)

