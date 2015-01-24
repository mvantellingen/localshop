from datetime import datetime
from md5 import md5


class PyPiXMLRPCStub():

    def package_releases(self, package_name, show_hidden=False):
        return ['0.4.0', '0.1']

    def search(self, query_dict):
        return [{'_pypi_ordering': 8,
                 'name': 'minibar',
                 'summary': 'Simple text progress bar library',
                 'version': '0.4.0'}]

    def release_data(self, package_name, version):
        return {
            '_pypi_hidden': False,
            '_pypi_ordering': 8,
            'author': 'Cesar Canassa',
            'author_email': 'cesar@canassa.com',
            'bugtrack_url': '',
            'cheesecake_code_kwalitee_id': None,
            'cheesecake_documentation_id': None,
            'cheesecake_installability_id': None,
            'classifiers': ['Development Status :: 3 - Alpha'],
            'description': 'Minibar',
            'docs_url': '',
            'download_url': 'UNKNOWN',
            'downloads': {'last_day': 342, 'last_month': 820, 'last_week': 457},
            'home_page': 'https://github.com/canassa/minibar',
            'keywords': 'progressbar progress bar',
            'license': 'MIT',
            'maintainer': None,
            'maintainer_email': None,
            'name': 'minibar',
            'package_url': 'http://pypi.python.org/pypi/minibar',
            'platform': 'UNKNOWN',
            'release_url': 'http://pypi.python.org/pypi/minibar/{}'.format(version),
            'requires_python': None,
            'stable_version': None,
            'summary': 'Simple text progress bar library',
            'version': version,
        }

    def package_urls(self, package_name, version):
        return [{
            'has_sig': False,
            'upload_time': datetime(2015, 1, 1, 12, 0, 0),
            'comment_text': '',
            'python_version': '3.4',
            'url': 'https://pypi.python.org/packages/3.4/m/minibar/minibar-{}-py2.py3-none-any.whl'.format(version),
            'md5_digest': md5(version).hexdigest(),
            'downloads': 208,
            'filename': 'minibar-{}-py2.py3-none-any.whl'.format(version),
            'packagetype': 'bdist_wheel',
            'size': 5844,
        },
        {
            'has_sig': False,
            'upload_time': datetime(2015, 1, 1, 12, 0, 0),
            'comment_text': '',
            'python_version': 'source',
            'url': 'https://pypi.python.org/packages/source/m/minibar/minibar-{}.tar.gz'.format(version),
            'md5_digest': md5(version).hexdigest(),
            'downloads': 223,
            'filename': 'minibar-{}.tar.gz'.format(version),
            'packagetype': 'sdist',
            'size': 3956,
        }]
