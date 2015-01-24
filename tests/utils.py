from datetime import datetime


DB = {
    'minibar': {
        'info': {
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
            'release_url': 'http://pypi.python.org/pypi/minibar/0.4.0',
            'requires_python': None,
            'stable_version': None,
            'summary': 'Simple text progress bar library',
            'version': '0.4.0',
        },
        'releases': {
            '0.4.0': [{
                'has_sig': False,
                'upload_time': datetime(2015, 1, 1, 12, 0, 0),
                'comment_text': '',
                'python_version': '3.4',
                'url': 'https://pypi.python.org/packages/3.4/m/minibar/minibar-0.4.0-py2.py3-none-any.whl',
                'md5_digest': '0bbdf41e028a4e6c75dfbd59660b6328',
                'downloads': 208,
                'filename': 'minibar-0.4.0-py2.py3-none-any.whl',
                'packagetype': 'bdist_wheel',
                'size': 5844,
            },
            {
                'has_sig': False,
                'upload_time': datetime(2015, 1, 1, 12, 0, 0),
                'comment_text': '',
                'python_version': 'source',
                'url': 'https://pypi.python.org/packages/source/m/minibar/minibar-0.4.0.tar.gz',
                'md5_digest': 'a3768a7f948871d8e47b146053265100',
                'downloads': 223,
                'filename': 'minibar-0.4.0.tar.gz',
                'packagetype': 'sdist',
                'size': 3956,
            }],
            '0.1': [{
                'has_sig': False,
                'upload_time': '2014-06-01T02:49:38',
                'comment_text': '',
                'python_version': 'source',
                'url': 'https://pypi.python.org/packages/source/m/minibar/minibar-0.1.tar.gz',
                'md5_digest': 'c935bfa49cb49e4f97fb8e24371105d7',
                'downloads': 876,
                'filename': 'minibar-0.1.tar.gz',
                'packagetype': 'sdist',
                'size': 3461,
            }],
        },
        'urls': [{
            'has_sig': False,
            'upload_time': '2015-01-16T17:13:55',
            'comment_text': '',
            'python_version': '3.4',
            'url': 'https://pypi.python.org/packages/3.4/m/minibar/minibar-0.4.0-py2.py3-none-any.whl',
            'md5_digest': '0bbdf41e028a4e6c75dfbd59660b6328',
            'downloads': 210,
            'filename': 'minibar-0.4.0-py2.py3-none-any.whl',
            'packagetype': 'bdist_wheel',
            'size': 5844,
        },
        {
            'has_sig': False,
            'upload_time': '2015-01-16T17:13:52',
            'comment_text': '',
            'python_version': 'source',
            'url': 'https://pypi.python.org/packages/source/m/minibar/minibar-0.4.0.tar.gz',
            'md5_digest': 'a3768a7f948871d8e47b146053265100',
            'downloads': 225,
            'filename': 'minibar-0.4.0.tar.gz',
            'packagetype': 'sdist',
            'size': 3956
        }],
    }
}


class PyPiXMLRPCStub():

    def package_releases(self, package_name, show_hidden=False):
        return DB[package_name]['releases'].keys()

    def search(self, query_dict):
        return [{'_pypi_ordering': 8,
                 'name': 'minibar',
                 'summary': 'Simple text progress bar library',
                 'version': '0.4.0'}]

    def release_data(self, package_name, version):
        return DB[package_name]['info']

    def package_urls(self, package_name, version):
        return DB[package_name]['releases'][version]
