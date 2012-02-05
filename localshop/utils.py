import inspect
import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.generic.base import View


def clean_redirect_url(request, url, default='/'):
    """ Use default setting if redirect_to is empty else do a
    security check -- don't allow redirection to a different
    host.

    """
    netloc = urlparse.urlparse(url)[1]
    if not url or (netloc and netloc != request.get_host()):
        url = default
    return url


def _perm_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)


def permission_required(perm, login_url=None, raise_exception=True):
    """Custom implementation of django's permission_required which also
    works as class decorator.

    """
    def _wrapper(func):
        perm_check = _perm_required(perm, login_url, raise_exception)
        if inspect.isclass(func) and issubclass(func, View):
            original_dispatch = func.dispatch

            @method_decorator(perm_check)
            def dispatch(cls, request, *args, **kwargs):
                return original_dispatch(cls, request, *args, **kwargs)
            func.dispatch = dispatch
            return func
        return perm_check(func)

    return _wrapper
