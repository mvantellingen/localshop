import logging
import os

from celery.task import task
from django.core.files import File
import requests

from localshop.apps.packages import models
from localshop.apps.packages.pypi import get_package_data


@task
def download_file(pk):
    release_file = models.ReleaseFile.objects.get(pk=pk)
    logging.info("Downloading %s", release_file.url)
    response = requests.get(release_file.url, stream=True)

    # Write the file to the django file field
    filename = os.path.basename(release_file.url)
    streaming_file = File(response.raw, filename)

    # Setting the size manually since Django can't figure it our from
    # the raw HTTPResponse
    if 'content-length' in response.headers:
        streaming_file.size = int(response.headers['content-length'])
    else:
        streaming_file.size = len(response.content)
    release_file.distribution.save(filename, streaming_file)
    release_file.save()
    logging.info("Complete")


@task
def update_packages():
    logging.info('Updated packages')
    for package in models.Package.objects.filter(is_local=False):
        logging.info('Updating package %s', package.name)
        get_package_data(package.name, package)
    logging.info('Complete')
