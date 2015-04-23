import mimetypes
import logging
import os

import requests
from celery.task import task
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.utils.timezone import now

from localshop.apps.packages import models, forms
from localshop.apps.packages.utils import md5_hash_file
from localshop.utils import no_duplicates, enqueue


@task(bind=True)
@no_duplicates
def fetch_package(self, slug):
    """
    """
    logging.info('start fetch_package: %s', slug)

    response = requests.get(settings.LOCALSHOP_PYPI_URL + '/{}/json'.format(slug))

    if response.status_code == 404:
        return

    if response.status_code != 200:
        return

    package_data = response.json()
    name = package_data['info']['name']

    try:
        package = models.Package.objects.get(name=name)
        releases = package.get_all_releases()
    except models.Package.DoesNotExist:
        package = models.Package(name=name)
        releases = {}

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
    logging.info('done fetch_package: %s', slug)


@task
def download_file(pk):
    """Download the file reference in `models.ReleaseFile` with the given pk.

    """
    release_file = models.ReleaseFile.objects.get(pk=pk)
    logging.info("Downloading %s", release_file.url)

    proxies = None
    if settings.LOCALSHOP_HTTP_PROXY:
        proxies = settings.LOCALSHOP_HTTP_PROXY
    response = requests.get(release_file.url, stream=True, proxies=proxies)

    # Write the file to the django file field
    filename = os.path.basename(release_file.url)

    # Setting the size manually since Django can't figure it our from
    # the raw HTTPResponse
    if 'content-length' in response.headers:
        size = int(response.headers['content-length'])
    else:
        size = len(response.content)

    # Setting the content type by first looking at the response header
    # and falling back to guessing it from the filename
    default_content_type = 'application/octet-stream'
    content_type = response.headers.get('content-type')
    if content_type is None or content_type == default_content_type:
        content_type = mimetypes.guess_type(filename)[0] or default_content_type

    # Using Django's temporary file upload system to not risk memory
    # overflows
    with TemporaryUploadedFile(name=filename, size=size, charset='utf-8',
                               content_type=content_type) as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)

        # Validate the md5 hash of the downloaded file
        md5_hash = md5_hash_file(temp_file)
        if md5_hash != release_file.md5_digest:
            logging.error("MD5 hash mismatch: %s (expected: %s)" % (
                md5_hash, release_file.md5_digest))
            return

        release_file.distribution.save(filename, temp_file)
        release_file.save()
    logging.info("Complete")


@task
def update_packages():
    """Update package information for all packages"""
    logging.info('Updated packages')
    for package in models.Package.objects.filter(is_local=False):
        logging.info('Updating package %s', package.name)
        enqueue(fetch_package, package.name)
    logging.info('Complete')
