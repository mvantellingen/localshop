import os.path

from django.test import TestCase
from django.utils import six
from storages.backends.overwrite import OverwriteStorage

from localshop.apps.packages import models
from localshop.apps.packages import utils
from localshop.utils import TemporaryMediaRootMixin

from tests import factories


class TestRepository(TestCase):
    def test_check_user_role_superuser(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory(is_superuser=True)
        user.is_superuser = True
        factories.TeamMemberFactory(user=user, team=team, role='developer')

        assert repository.check_user_role(user, ['owner'])

    def test_check_user_role_owner(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='owner')
        assert repository.check_user_role(user, ['owner'])

    def test_check_user_role_wrong_role(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='developer')
        assert not repository.check_user_role(user, ['owner'])

    def test_check_user_role_multiple_roles(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='developer')
        assert repository.check_user_role(user, ['owner', 'developer'])

    def test_simple_index_url(self):
        repository = factories.RepositoryFactory(slug='foobar')
        assert repository.simple_index_url == '/repo/foobar'


class TestRelease(TestCase):
    def test_description_html(self):
        release = factories.ReleaseFactory(description='foobar')
        assert release.description_html == '<p>foobar</p>\n'


class TestReleaseFile(TemporaryMediaRootMixin, TestCase):
    def setUp(self):
        super(TestReleaseFile, self).setUp()

        field = [field for field in models.ReleaseFile._meta.fields
                    if field.name == 'distribution'][0]
        field.storage = OverwriteStorage()

    def test_save_contents(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = six.BytesIO(six.b("release-file-contents"))
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertEqual(
            release_file.distribution.name, '2.7/t/test-package/dummy.txt')
        self.assertTrue(os.path.exists(release_file.distribution.path))

    def test_delete_file(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = six.BytesIO(six.b("release-file-contents"))
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertTrue(os.path.exists(release_file.distribution.path))

        utils.delete_files(models.ReleaseFile, instance=release_file)
        self.assertFalse(os.path.exists(release_file.distribution.path))

    def test_delete_file_twice_referenced(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = six.BytesIO(six.b("release-file-contents"))
        release_file.save_filecontent('dummy.txt', dummy_fh)

        release_file = factories.ReleaseFileFactory(
            release=release_file.release, filetype='bdist_egg')
        release_file.save_filecontent('dummy.txt', dummy_fh)

        self.assertTrue(os.path.exists(release_file.distribution.path))

        utils.delete_files(models.ReleaseFile, instance=release_file)

        # File should still exist
        self.assertTrue(os.path.exists(release_file.distribution.path))
