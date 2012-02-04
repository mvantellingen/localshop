import os

from django.db import models
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils.models import TimeStampedModel


class Package(models.Model):
    created = AutoCreatedField(db_index=True)

    modified = AutoLastModifiedField()

    name = models.SlugField(max_length=200, unique=True)

    uptime_timestamp = models.DateTimeField(null=True)

    def get_all_releases(self):
        result = {}
        for release in self.releases.all():
            files = dict((r.filename, r) for r in release.files.all())
            result[release.version] = (release, files)
        return result


class Release(models.Model):

    created = AutoCreatedField()
    modified = AutoLastModifiedField()

    package = models.ForeignKey(Package, related_name="releases")
    version = models.CharField(max_length=512)


def release_file_upload_to(instance, filename):
    return os.path.join(instance.release.package.name, filename)


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

    type = models.CharField(max_length=25, choices=TYPES)

    file = models.FileField(upload_to=release_file_upload_to, max_length=512)

    filename = models.CharField(max_length=200, blank=True, null=True)

    digest = models.CharField(max_length=512)

    python_version = models.CharField(max_length=25)

    url = models.URLField(max_length=1024, blank=True)

    class Meta:
        unique_together = ("release", "type", "python_version", "filename")

    def get_absolute_url(self):
        url = reverse('packages:download', kwargs={
            'pk': self.pk, 'filename': self.filename
        })
        return '%s#md5=%s' % (url, self.digest)
