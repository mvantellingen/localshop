from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from localshop.packages import models
from localshop.packages import views


class TestDistutilsViews(TestCase):

    def test_register_new(self):
        post = MultiValueDict({
            'name': ['localshop'],
            'license': ['BSD'],
            'author': ['Michael van Tellingen'],
            'home_page': ['http://github.com/mvantellingen/localshop'],
            ':action': ['submit'],
            'download_url': [None],
            'summary': [
                'A private pypi server including auto-mirroring of pypi.'],
            'author_email': ['michaelvantellingen@gmail.com'],
            'metadata_version': ['1.0'],
            'version': ['0.1'],
            'platform': [None],
            'classifiers': [
                'Development Status :: 2 - Pre-Alpha',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'Intended Audience :: System Administrators',
                'Operating System :: OS Independent',
                'Topic :: Software Development'
            ],
            'description': [None]
        })
        files = MultiValueDict()

        user = User.objects.create_user('john', 'john@example.org', 'secret')
        response = views.handle_register_or_upload(post, files, user)
        self.assertEqual(response.status_code, 200, response.content)

        package = models.Package.objects.get(name='localshop')
        self.assertEqual(package.releases.count(), 1)

    def test_upload_new(self):
        post = MultiValueDict({
            'name': ['localshop'],
            'license': ['BSD'],
            'author': ['Michael van Tellingen'],
            'home_page': ['http://github.com/mvantellingen/localshop'],
            ':action': ['submit'],
            'download_url': [None],
            'summary': [
                'A private pypi server including auto-mirroring of pypi.'],
            'author_email': ['michaelvantellingen@gmail.com'],
            'metadata_version': ['1.0'],
            'version': ['0.1'],
            'platform': [None],
            'classifiers': [
                'Development Status :: 2 - Pre-Alpha',
                'Framework :: Django',
                'Intended Audience :: Developers',
                'Intended Audience :: System Administrators',
                'Operating System :: OS Independent',
                'Topic :: Software Development'
            ],
            'description': [None],

            # Extra fields for upload
            'pyversion': [''],
            'filetype': ['sdist'],
            'md5_digest': ['dc8f0311bb830ee96b8627f8335f2cb1'],
        })
        files = MultiValueDict({
            'distribution': [
                SimpleUploadedFile(
                    'localshop-0.1.tar.gz', 'binary-test-data-here')
            ]
        })

        user = User.objects.create_user('john', 'john@example.org', 'secret')
        response = views.handle_register_or_upload(post, files, user)
        self.assertEqual(response.status_code, 200, response.content)

        package = models.Package.objects.get(name='localshop')
        self.assertEqual(package.releases.count(), 1)
        self.assertTrue(package.is_local)

        release = package.releases.all()[0]
        self.assertEqual(release.files.count(), 1)

        release_file = release.files.all()[0]
        self.assertEqual(release_file.python_version, 'source')
        self.assertEqual(release_file.filetype, 'sdist')
        self.assertEqual(release_file.md5_digest,
            'dc8f0311bb830ee96b8627f8335f2cb1')
        self.assertEqual(release_file.filename, 'localshop-0.1.tar.gz')
        self.assertEqual(release_file.distribution.read(),
            'binary-test-data-here')
