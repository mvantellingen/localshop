import logging

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponseForbidden

from localshop.apps.permissions.utils import authenticate_user
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

        if self.repository.cidr_list.has_access(ip_addr, with_credentials=False):
            return super(RepositoryAccessMixin, self).dispatch(
                request, *args, **kwargs)

        if not self.repository.cidr_list.has_access(ip_addr, with_credentials=True):
            return HttpResponseForbidden('No permission')

        # Just return the original view because already logged in
        if request.user.is_authenticated():
            return super(RepositoryAccessMixin, self).dispatch(
                request, *args, **kwargs)

        user = authenticate_user(request)
        if user is not None:
            login(request, user)
            return super(RepositoryAccessMixin, self).dispatch(
                request, *args, **kwargs)

        return HttpResponseUnauthorized(content='Authorization Required')
