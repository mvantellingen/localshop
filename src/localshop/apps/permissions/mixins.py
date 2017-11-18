import logging

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponseForbidden

from localshop.apps.permissions.utils import (
    authenticate_user, get_basic_auth_data)
from localshop.http import HttpResponseUnauthorized

logger = logging.getLogger(__name__)


class RepositoryAccessMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # TODO: Should be handled in middleware
        if settings.LOCALSHOP_USE_PROXIED_IP:
            try:
                ip_addr = request.META['HTTP_X_FORWARDED_FOR']
            except KeyError:
                return HttpResponseForbidden('No permission')
            else:
                # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
                # The client's IP will be the first one.
                ip_addr = ip_addr.split(",")[0].strip()
        else:
            ip_addr = request.META['REMOTE_ADDR']

        logger.info("Package request from %s", ip_addr)

        # Check repository based credentials, move to middleware ?
        request.credentials = None
        key, secret = get_basic_auth_data(request)

        if not (key and secret) and request.method == 'POST':
            # post means register or upload,
            # distutils for register do not sent the auth by default
            # so force it to send HTTP_AUTHORIZATION header
            return HttpResponseUnauthorized()

        if key and secret:
            credential = self.repository.credentials.authenticate(key, secret)
            if credential:
                request.credentials = credential

            else:

                # Might be a regular django user, this should be deprecated as
                # it is just not secure enough. We need to start using user
                # credentials for this.
                user = authenticate_user(request)
                if user:
                    login(request, user)
                else:
                    return HttpResponseUnauthorized()

        if self._allow_request(request, ip_addr):
            return super(RepositoryAccessMixin, self).dispatch(
                request, *args, **kwargs)

        return HttpResponseUnauthorized("No permission")


    def _allow_request(self, request, ip_addr):
        # If the user is already logged in then continue
        if request.user.is_authenticated():
            return True

        # If this view doesn't require upload permissions then we allow access
        # purely based on the cidr. Otherwise credentials are required
        if self.repository.cidr_list.has_access(ip_addr, with_credentials=False):
            return True

        elif self.repository.cidr_list.has_access(ip_addr, with_credentials=True):
            return bool(request.credentials)

        return False
