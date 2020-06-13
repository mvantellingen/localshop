import os.path

import pytest
from django.utils import six

from localshop.apps.packages import models, utils
from tests import factories


class TestRepository:

    @pytest.mark.django_db
    def test_check_user_role_superuser(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory(is_superuser=True)
        user.is_superuser = True
        factories.TeamMemberFactory(user=user, team=team, role='developer')

        assert repository.check_user_role(user, ['owner'])

    @pytest.mark.django_db
    def test_check_user_role_owner(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='owner')
        assert repository.check_user_role(user, ['owner'])

    @pytest.mark.django_db
    def test_check_user_role_wrong_role(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='developer')
        assert not repository.check_user_role(user, ['owner'])

    @pytest.mark.django_db
    def test_check_user_role_multiple_roles(self):
        repository = factories.RepositoryFactory()
        team = factories.TeamFactory()
        repository.teams.add(team)

        user = factories.UserFactory()
        factories.TeamMemberFactory(user=user, team=team, role='developer')
        assert repository.check_user_role(user, ['owner', 'developer'])


class TestReleaseFile:

    @pytest.fixture(autouse=True)
    def media_root(self, tmpdir, settings):
        settings.MEDIA_ROOT = tmpdir

    @pytest.mark.django_db
    def test_save_contents(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = six.BytesIO(six.b("release-file-contents"))
        release_file.save_filecontent('dummy.txt', dummy_fh)

        assert release_file.distribution.name == 'default/2.7/T/Test_Package/dummy.txt'
        assert os.path.exists(release_file.distribution.path)

    @pytest.mark.django_db
    def test_delete_file(self):
        release_file = factories.ReleaseFileFactory()

        dummy_fh = six.BytesIO(six.b("release-file-contents"))
        release_file.save_filecontent('dummy.txt', dummy_fh)

        assert os.path.exists(release_file.distribution.path)

        utils.delete_files(models.ReleaseFile, instance=release_file)
        assert not os.path.exists(release_file.distribution.path)

    @pytest.mark.skip
    @pytest.mark.django_db
    def test_delete_file_twice_referenced(self):
        dummy_fh = six.BytesIO(six.b("release-file-contents"))

        release_file = factories.ReleaseFileFactory()
        release_file.save_filecontent('dummy.txt', dummy_fh)

        release_file = factories.ReleaseFileFactory(
            release=release_file.release, filetype='bdist_egg')
        release_file.save_filecontent('dummy.txt', dummy_fh)

        assert os.path.exists(release_file.distribution.path)

        utils.delete_files(models.ReleaseFile, instance=release_file)

        # File should still exist
        assert os.path.exists(release_file.distribution.path)
