import logging
import re
import requests
import xmlrpclib
from copy import copy
from StringIO import StringIO

from django.conf import settings

from localshop.utils import now
from localshop.apps.packages import forms
from localshop.apps.packages import models


logger = logging.getLogger(__name__)


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


def get_package_data(name, package=None):
    """Retrieve metadata information for the given package name"""

    response = requests.get(settings.LOCALSHOP_PYPI_URL + '/{}/json'.format(name))

    if response.status_code == 404:
        return

    if response.status_code != 200:
        return

    package_data = response.json()
    name = package_data['info']['name']

    if not package:
        package = models.Package(name=name)
        releases = {}
    else:
        releases = package.get_all_releases()

    # If the matched package differs from the name we tried to retrieve then
    # retry to fetch the package from the database.
    if package.name != name:
        try:
            package = models.Package.objects.get(name=package.name)
        except models.Package.objects.DoesNotExist:
            pass

    # Save the package if it is new
    if not package.pk:
        package.save()

    for version, release_list in package_data['releases'].items():
        release, files = releases.get(version, (None, {}))
        if not release:
            release = models.Release(package=package, version=version)
            release.save()

        release_data = {
            'author': package_data['info']['author'],
            'author_email': package_data['info']['author_email'],
            'description': package_data['info']['description'],
            'download_url': package_data['info']['download_url'],
            'home_page': package_data['info']['home_page'],
            'license': package_data['info']['license'],
            'summary': package_data['info']['summary'],
            'version': version,
        }

        release_form = forms.PypiReleaseDataForm(release_data, instance=release)
        if release_form.is_valid():
            release_form.save()

        for data in release_list:
            release_file = files.get(data['filename'])
            if not release_file:
                release_file = models.ReleaseFile(
                    release=release, filename=data['filename'])

            release_file.python_version = data['python_version']
            release_file.filetype = data['packagetype']
            release_file.url = data['url']
            release_file.size = data['size']
            release_file.md5_digest = data['md5_digest']
            release_file.save()

    package.update_timestamp = now()
    package.save()
    return package
