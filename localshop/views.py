
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from localshop.apps.packages.models import Release, ReleaseFile
from localshop.apps.packages import xmlrpc


@csrf_exempt
def index(request):
    if request.method == 'POST':
        return xmlrpc.handle_request(request)
    return redirect('dashboard:index')


class LoginRequiredMixin(object):
    """
    View mixin that applies the login_required decorator
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which uses the permission_required decorator.
    """
    permission_required = None  # the permission, e.g. 'auth.add_user'
    raise_exception = True  # raises a 403 exception by default
    login_url = settings.LOGIN_URL  # the url to redirect to

    def dispatch(self, request, *args, **kwargs):
        if (self.permission_required is None or
                '.' not in self.permission_required):
            raise ImproperlyConfigured("PermissionRequiredMixin must have a "
                                       "permission_required attribute.")
        decorator = permission_required(self.permission_required,
                                        self.login_url, self.raise_exception)
        decorated_dispatch = decorator(super(PermissionRequiredMixin, self).dispatch)
        return decorated_dispatch(request, *args, **kwargs)
