import datetime
import xmlrpclib

from localshop.packages import models


def get_package_urls(slug, package=None):
    if not package:
        package = models.Package(name=slug)
        releases = {}
    else:
        releases = package.get_all_releases()

    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    versions = client.package_releases(package.name, True)

    # package_releases() method is case-sensitive, if nothing found
    # then we search for it
    # XXX: Ask pypi to make it case-insensitive?
    if not versions:
        for item in client.search({'name': slug}):
            if slug == item['name'].lower():
                package.name = slug = item['name']
                break
        else:
            return

        # Retry retrieving the versions with the new/correct name
        versions = client.package_releases(package.name, True)

    # Save the package if it is new
    if not package.pk:
        package.save()

    for version in versions:
        release, files = releases.get(version, (None, {}))
        if not release:
            release = models.Release(package=package, version=version)
            release.save()

        release_files = client.package_urls(package.name, release.version)
        for info in release_files:
            release_file = files.get(info['filename'])
            if not release_file:
                release_file = models.ReleaseFile(
                    release=release, filename=info['filename'])

            release_file.python_version = info['python_version']
            release_file.type = info['packagetype']
            release_file.url = info['url']
            release_file.size = info['size']
            release_file.digest = info['md5_digest']
            release_file.save()

    package.update_timestamp = datetime.datetime.utcnow()
    return package
