import factory
from django.contrib.auth import get_user_model

from localshop.apps.accounts.models import Team, TeamMember
from localshop.apps.packages.models import (
    Package, Release, ReleaseFile, Repository)
from localshop.apps.permissions.models import CIDR, Credential


class RepositoryFactory(factory.DjangoModelFactory):
    name = 'Default'
    slug = 'default'

    class Meta:
        model = Repository
        django_get_or_create = ('slug',)


class PackageFactory(factory.DjangoModelFactory):
    name = 'Test_Package'
    normalized_name = 'test-package'
    repository = factory.SubFactory(RepositoryFactory)

    class Meta:
        model = Package


class ReleaseFactory(factory.DjangoModelFactory):
    author = 'John Doe'
    author_email = 'j.doe@example.org'
    description = 'A test release'
    download_url = 'http://www.example.org/download'
    home_page = 'http://www.example.org'
    license = 'BSD'
    metadata_version = '1.0'
    package = factory.SubFactory(PackageFactory)
    summary = 'Summary of the test package'
    version = '1.0.0'

    class Meta:
        model = Release


class ReleaseFileFactory(factory.DjangoModelFactory):
    release = factory.SubFactory(ReleaseFactory)
    distribution = factory.django.FileField(filename='the_file.dat',
                                            data='the file data')
    size = 1120
    filetype = 'sdist'
    filename = factory.LazyAttribute(lambda a: 'test-%s-%s.zip' % (
        a.release.version, a.filetype))
    md5_digest = '62ecd3ee980023db87945470aa2b347b'
    python_version = '2.7'
    requires_python = 'py2'
    url = factory.LazyAttribute(lambda a: (
        'http://www.example.org/download/%s' % a.filename))

    class Meta:
        model = ReleaseFile


class CIDRFactory(factory.DjangoModelFactory):
    repository = factory.SubFactory(RepositoryFactory)
    cidr = '0/0'
    require_credentials = False

    class Meta:
        model = CIDR


class CredentialFactory(factory.DjangoModelFactory):
    class Meta:
        model = Credential


class TeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = Team


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()


class TeamMemberFactory(factory.DjangoModelFactory):
    team = factory.SubFactory(TeamFactory)
    user = factory.SubFactory(UserFactory)
    role = 'developer'

    class Meta:
        model = TeamMember
