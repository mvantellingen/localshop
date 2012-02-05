from mock import Mock

from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from localshop.packages.utils import parse_distutils_request


class TestParseDistutilsRequest(TestCase):
    def test_register_post(self):
        data = (
            '\n----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="license"\n\n'
            'BSD\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="name"\n\nlocalshop\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="metadata_version"\n\n'
            '1.0\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="author"\n\n'
            'Michael van Tellingen\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="home_page"\n\n'
            'http://github.com/mvantellingen/localshop\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name=":action"\n\n'
            'submit\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="download_url"\n\n'
            'UNKNOWN\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="summary"\n\n'
            'A private pypi server including auto-mirroring of pypi.\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="author_email"\n\n'
            'michaelvantellingen@gmail.com\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="version"\n\n'
            '0.1\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="platform"\n\n'
            'UNKNOWN\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Development Status :: 2 - Pre-Alpha\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Framework :: Django\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Intended Audience :: Developers\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Intended Audience :: System Administrators\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Operating System :: OS Independent\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="classifiers"\n\n'
            'Topic :: Software Development\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254\n'
            'Content-Disposition: form-data; name="description"\n\n'
            'UNKNOWN\n'
            '----------------GHSKFJDLGDS7543FJKLFHRE75642756743254--\n'
        )
        request = Mock()
        request.raw_post_data = data
        post, files = parse_distutils_request(request)

        expected_post = MultiValueDict({
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
        expected_files = MultiValueDict()

        self.assertEqual(post, expected_post)
        self.assertEqual(files, expected_files)
