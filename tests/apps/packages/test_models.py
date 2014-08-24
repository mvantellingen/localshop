import os.path
from cStringIO import StringIO

from django.test import TestCase
from storages.backends.overwrite import OverwriteStorage

from localshop.apps.packages import models
from localshop.apps.packages import utils
from localshop.utils import TemporaryMediaRootMixin

from tests.apps.packages import factories


class TestReleaseFile(TemporaryMediaRootMixin, TestCase):
    def setUp(self):
        super(TestReleaseFile, self).setUp()

        field = [field for field in models.ReleaseFile._meta.fields
                    if field.name == 'distribution'][0]
        field.storage = OverwriteStorage()

    def test_save_contents(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = StringIO("release-file-contents")
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertEqual(
            release_file.distribution.name, '2.7/t/test-package/dummy.txt')
        self.assertTrue(os.path.exists(release_file.distribution.path))

    def test_delete_file(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = StringIO("release-file-contents")
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertTrue(os.path.exists(release_file.distribution.path))

        utils.delete_files(models.ReleaseFile, instance=release_file)
        self.assertFalse(os.path.exists(release_file.distribution.path))

    def test_delete_file_twice_referenced(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = StringIO("release-file-contents")
        release_file.save_filecontent('dummy.txt', dummy_fh)

        release_file = factories.ReleaseFileFactory(
            release=release_file.release, filetype='bdist_egg')
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertTrue(os.path.exists(release_file.distribution.path))

        utils.delete_files(models.ReleaseFile, instance=release_file)

        # File should still exist
        self.assertTrue(os.path.exists(release_file.distribution.path))
