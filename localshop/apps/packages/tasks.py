import mimetypes
import logging
import os

import requests
from celery.task import task
from django.conf import settings
from django.core.files.uploadedfile import TemporaryUploadedFile

from localshop.apps.packages import models
from localshop.apps.packages.pypi import get_package_data
from localshop.apps.packages.utils import md5_hash_file


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
        get_package_data(package.name, package)
    logging.info('Complete')
