from functools import wraps

from django.contrib.auth import login, authenticate
from django.utils.decorators import available_attrs
from django.http import HttpResponseForbidden
from django.db import DataError, DatabaseError

from localshop.apps.permissions.models import CIDR
from localshop.http import HttpResponseUnauthorized


def decode_credentials(auth):
    auth = auth.strip().decode('base64')
    return auth.split(':', 1)


def split_auth(request):
    auth = request.META.get('HTTP_AUTHORIZATION')
    if auth:
        method, identity = auth.split(' ', 1)
    else:
        method, identity = None, None
    return method, identity


def authenticate_user(request):
    method, identity = split_auth(request)
    if method is not None and method.lower() == 'basic':
        key, secret = decode_credentials(identity)
        try:
            user = authenticate(access_key=key, secret_key=secret)
        except (DatabaseError, DataError):
            # we fallback on django user auth in case of DB error
            user = None
        if not user:
            user = authenticate(username=key, password=secret)
        return user


def credentials_required(view_func):
    """
    This decorator should be used with views that need simple authentication
    against Django's authentication framework.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def decorator(request, *args, **kwargs):
        ip_addr = request.META['REMOTE_ADDR']

        if CIDR.objects.has_access(ip_addr, with_credentials=False):
            return view_func(request, *args, **kwargs)

        if not CIDR.objects.has_access(ip_addr, with_credentials=True):
            return HttpResponseForbidden('No permission')

        # Just return the original view because already logged in
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        user = authenticate_user(request)
        if user is not None:
            login(request, user)
            return view_func(request, *args, **kwargs)

        return HttpResponseUnauthorized(content='Authorization Required')
    return decorator
