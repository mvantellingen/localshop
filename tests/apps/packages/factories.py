import factory

from localshop.apps.packages import models


class PackageFactory(factory.DjangoModelFactory):
    name = 'test-package'

    class Meta:
        model = models.Package


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
        model = models.Release


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
    url = factory.LazyAttribute(lambda a: (
        'http://www.example.org/download/%s' % a.filename))

    class Meta:
        model = models.ReleaseFile
