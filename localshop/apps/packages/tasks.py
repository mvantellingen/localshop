import logging
import os
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from django.core.files import File

from celery.task import task
import requests

from localshop.apps.packages import models
from localshop.apps.packages.pypi import get_package_data


@task
def download_file(pk):
    release_file = models.ReleaseFile.objects.get(pk=pk)
    logging.info("Downloading %s", release_file.url)
    response = requests.get(release_file.url, prefetch=False)

    # Store the content in a temporary file
    tmp_file = NamedTemporaryFile()
    copyfileobj(response.raw, tmp_file)

    # Write the file to the django file field
    filename = os.path.basename(release_file.url)
    release_file.distribution.save(filename, File(tmp_file))
    release_file.save()
    logging.info("Complete")


@task
def update_packages():
    logging.info('Updated packages')
    for package in models.Package.objects.filter(is_local=False):
        logging.info('Updating package %s', package.name)
        get_package_data(package.name, package)
    logging.info('Complete')
