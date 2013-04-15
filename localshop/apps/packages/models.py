import docutils.core
import logging
import os
from docutils.utils import SystemMessage
from shutil import copyfileobj
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.core.files import File
from django.core.files.storage import get_storage_class
from django.core.urlresolvers import reverse
from django.utils.functional import LazyObject
from django.utils.html import escape
from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from localshop.apps.packages.signals import release_file_notfound
from localshop.apps.packages.utils import delete_files


logger = logging.getLogger(__name__)


class Classifier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Package(models.Model):
    created = AutoCreatedField(db_index=True)

    modified = AutoLastModifiedField()

    name = models.SlugField(max_length=200, unique=True)

    #: Indicate if this package is local (a private package)
    is_local = models.BooleanField(default=False)

    #: Timestamp when we last retrieved the metadata
    update_timestamp = models.DateTimeField(null=True)

    owners = models.ManyToManyField(User)

    class Meta:
        ordering = ['name']
        permissions = (
            ("view_package", "Can view package"),
        )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('packages:detail', None, {'name': self.name})

    def get_all_releases(self):
        result = {}
        for release in self.releases.all():
            files = dict((r.filename, r) for r in release.files.all())
            result[release.version] = (release, files)
        return result

    @property
    def last_release(self):
        return self.releases.order_by('-created')[0]


class Release(models.Model):

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    author = models.CharField(max_length=128, blank=True)

    author_email = models.CharField(max_length=255, blank=True)

    classifiers = models.ManyToManyField(Classifier)

    description = models.TextField(blank=True)

    download_url = models.CharField(max_length=200, blank=True, null=True)

    home_page = models.CharField(max_length=200, blank=True, null=True)

    license = models.TextField(blank=True)

    metadata_version = models.CharField(max_length=64, default=1.0)

    package = models.ForeignKey(Package, related_name="releases")

    summary = models.TextField(blank=True)

    user = models.ForeignKey(User, null=True)

    version = models.CharField(max_length=512)

    class Meta:
        ordering = ['-version']

    def __unicode__(self):
        return self.version

    @property
    def description_html(self):
        try:
            parts = docutils.core.publish_parts(
                self.description, writer_name='html4css1')
            return parts['fragment']
        except SystemMessage:
            desc = escape(self.description)
            return '<pre>%s</pre>' % desc


def release_file_upload_to(instance, filename):
    package = instance.release.package
    assert package.name and instance.python_version
    return os.path.join(
        instance.python_version,
        package.name[0],
        package.name,
        filename)


class DistributionStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(
            settings.LOCALSHOP_DISTRIBUTION_STORAGE)()


class ReleaseFile(models.Model):

    TYPES = Choices(
        ('sdist', 'Source'),
        ('bdist_egg', 'Egg'),
        ('bdist_msi', 'MSI'),
        ('bdist_dmg', 'DMG'),
        ('bdist_rpm', 'RPM'),
        ('bdist_dumb', 'bdist_dumb'),
        ('bdist_wininst', 'bdist_wininst'),
        ('bdist_wheel', 'bdist_wheel'),
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    release = models.ForeignKey(Release, related_name="files")

    size = models.IntegerField(null=True)

    filetype = models.CharField(max_length=25, choices=TYPES)

    distribution = models.FileField(upload_to=release_file_upload_to,
        storage=DistributionStorage(), max_length=512)

    filename = models.CharField(max_length=200, blank=True, null=True)

    md5_digest = models.CharField(max_length=512)

    python_version = models.CharField(max_length=25)

    url = models.CharField(max_length=1024, blank=True)

    user = models.ForeignKey(User, null=True)

    class Meta:
        unique_together = ('release', 'filetype', 'python_version', 'filename')

    def __unicode__(self):
        return self.filename

    def get_absolute_url(self):
        url = reverse('packages:download', kwargs={
            'name': self.release.package.name,
            'pk': self.pk, 'filename': self.filename
        })
        return '%s#md5=%s' % (url, self.md5_digest)

    def save_filecontent(self, filename, fh):
        tmp_file = NamedTemporaryFile()
        copyfileobj(fh, tmp_file)
        self.distribution.save(filename, File(tmp_file))


if settings.LOCALSHOP_DELETE_FILES:
    post_delete.connect(
        delete_files, sender=ReleaseFile,
        dispatch_uid="localshop.apps.packages.utils.delete_files")


def download_missing_release_file(sender, release_file, **kwargs):
    """Start a celery task to download the release file from pypi.

    If `settings.LOCALSHOP_ISOLATED` is True then download the file in-process.

    """
    from .tasks import download_file
    if not settings.LOCALSHOP_ISOLATED:
        download_file.delay(pk=release_file.pk)
    else:
        download_file(pk=release_file.pk)

release_file_notfound.connect(download_missing_release_file,
    dispatch_uid='localshop_download_release_file')
