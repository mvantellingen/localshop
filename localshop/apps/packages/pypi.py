import logging
import re
import xmlrpclib

from localshop.utils import now
from localshop.apps.packages import forms
from localshop.apps.packages import models


logger = logging.getLogger(__name__)


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
    if not package:
        package = models.Package(name=name)
        releases = {}
    else:
        releases = package.get_all_releases()

    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

    versions = client.package_releases(package.name, True)

    # package_releases() method is case-sensitive, if nothing found
    # then we search for it
    # XXX: Ask pypi to make it case-insensitive?
    names = get_search_names(name)
    if not versions:
        for item in client.search({'name': names}):
            if item['name'].lower() in [n.lower() for n in names]:
                package.name = name = item['name']
                break
        else:
            logger.info("No packages found matching %r", name)
            return

        # Retry retrieving the versions with the new/correct name
        versions = client.package_releases(package.name, True)

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

    for version in versions:
        release, files = releases.get(version, (None, {}))
        if not release:
            release = models.Release(package=package, version=version)
            release.save()

        data = client.release_data(package.name, release.version)

        release_form = forms.PypiReleaseDataForm(data, instance=release)
        if release_form.is_valid():
            release_form.save()

        release_files = client.package_urls(package.name, release.version)
        for info in release_files:
            release_file = files.get(info['filename'])
            if not release_file:
                release_file = models.ReleaseFile(
                    release=release, filename=info['filename'])

            release_file.python_version = info['python_version']
            release_file.filetype = info['packagetype']
            release_file.url = info['url']
            release_file.size = info['size']
            release_file.md5_digest = info['md5_digest']
            release_file.save()

    package.update_timestamp = now()
    package.save()
    return package
