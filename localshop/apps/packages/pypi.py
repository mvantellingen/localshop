import re
import requests
import xmlrpclib
from copy import copy
from StringIO import StringIO


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
            fh = StringIO(response.content)
            return self.parse_response(fh)


def get_search_names(name):
    """Return a list of values to search on when we are looking for a package
    with the given name.

    This is required to search on both pyramid_debugtoolbar and
    pyramid-debugtoolbar.

    """
    parts = re.split('[-_]', name)
    if len(parts) == 1:
        return parts

    result = set()
    for i in range(len(parts) - 1, 0, -1):
        for s1 in '-_':
            prefix = s1.join(parts[:i])
            for s2 in '-_':
                suffix = s2.join(parts[i:])
                for s3 in '-_':
                    result.add(s3.join([prefix, suffix]))
    return list(result)
