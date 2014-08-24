import factory

from localshop.apps.packages import models


class PackageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Package

    name = 'test-package'


class ReleaseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Release

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


class ReleaseFileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.ReleaseFile

    release = factory.SubFactory(ReleaseFactory)
    size = 1120
    filetype = 'sdist'
    filename = factory.LazyAttribute(lambda a: 'test-%s-%s.zip' % (
        a.release.version, a.filetype))
    md5_digest = '62ecd3ee980023db87945470aa2b347b'
    python_version = '2.7'
    url = factory.LazyAttribute(lambda a: (
        'http://www.example.org/download/%s' % a.filename))
