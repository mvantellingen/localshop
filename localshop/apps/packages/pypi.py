import re
import requests
from copy import copy

from django.utils import six

if six.PY2:
    import xmlrpclib
else:
    import xmlrpc.client as xmlrpclib


class RequestTransport(xmlrpclib.Transport, object):
    """Custom transport (using requests) for the XMLRPC connection."""

    def __init__(self, use_datetime=0, proxies=None):
        super(RequestTransport, self).__init__(use_datetime)
        self.session = requests.Session()
        self.configure_requests(proxies=proxies)

    def configure_requests(self, proxies=None):
        self.session.headers.update({
            'Content-Type': 'text/xml',
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'identity',
        })
        self.session.proxies = copy(proxies)

    def set_proxy(self, proxies):
        self.session.proxies = copy(proxies)

    def request(self, host, handler, request_body, verbose=0):
        response = self.session.post(
            'https://%s%s' % (host, handler), data=request_body)

        if response.status_code == 200:
            self.verbose = verbose
            fh = six.StringIO(response.content)
            return self.parse_response(fh)


def normalize_name(name):
    return re.sub(r'[-_.]+', '-', name).lower()
