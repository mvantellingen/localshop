import os

import docutils.core
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField

from localshop.packages.utils import OverwriteStorage


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

    home_page = models.URLField(verify_exists=False, blank=True, null=True)

    license = models.TextField(blank=True)

    metadata_version = models.CharField(max_length=64, default=1.0)

    package = models.ForeignKey(Package, related_name="releases")

    summary = models.TextField(blank=True)

    user = models.ForeignKey(User, null=True)

    version = models.CharField(max_length=512)

    @property
    def description_html(self):
        parts = docutils.core.publish_parts(
            self.description, writer_name='html4css1')
        return parts['fragment']


def release_file_upload_to(instance, filename):
    package = instance.release.package
    assert package.name and instance.python_version
    return os.path.join(
        instance.python_version,
        package.name[0],
        package.name,
        filename)


class ReleaseFile(models.Model):

    TYPES = Choices(
        ('sdist', 'Source'),
        ('bdist_egg', 'Egg'),
        ('bdist_msi', 'MSI'),
        ('bdist_dmg', 'DMG'),
        ('bdist_rpm', 'RPM'),
        ('bdist_dumb', 'bdist_dumb'),
        ('bdist_wininst', 'bdist_wininst'),
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    release = models.ForeignKey(Release, related_name="files")

    size = models.IntegerField(null=True)

    filetype = models.CharField(max_length=25, choices=TYPES)

    distribution = models.FileField(upload_to=release_file_upload_to,
        storage=OverwriteStorage(), max_length=512)

    filename = models.CharField(max_length=200, blank=True, null=True)

    md5_digest = models.CharField(max_length=512)

    python_version = models.CharField(max_length=25)

    url = models.URLField(max_length=1024, blank=True)

    user = models.ForeignKey(User, null=True)

    class Meta:
        unique_together = ('release', 'filetype', 'python_version', 'filename')

    def get_absolute_url(self):
        url = reverse('packages:download', kwargs={
            'name': self.release.package.name,
            'pk': self.pk, 'filename': self.filename
        })
        return '%s#md5=%s' % (url, self.md5_digest)
