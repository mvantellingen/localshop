from io import StringIO
import json


class NamedStringIO(StringIO):

    """A StringIO that has a name in it"""

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super(NamedStringIO, self).__init__(*args, **kwargs)


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
                'upload_time': '2014-06-02T16:24:33',
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
                'upload_time': '2014-06-02T16:24:33',
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
    },
    'pyramid_debugtoolbar': {
        'info': {
            'maintainer': None,
            'docs_url': '',
            'requires_python': None,
            'maintainer_email': None,
            'cheesecake_code_kwalitee_id': None,
            'keywords': 'wsgi pylons pyramid transaction',
            'package_url': 'http://pypi.python.org/pypi/pyramid_debugtoolbar',
            'author': 'Chris McDonough, Michael Merickel, Casey Duncan, Blaise Laflamme',
            'author_email': 'pylons-devel@googlegroups.com',
            'download_url': 'UNKNOWN',
            'platform': 'UNKNOWN',
            'version': '2.3',
            'cheesecake_documentation_id': None,
            '_pypi_hidden': False,
            'description': '',
            'release_url': 'http://pypi.python.org/pypi/pyramid_debugtoolbar/2.3',
            'downloads': {
                'last_month': 21891,
                'last_week': 1452,
                'last_day': 44
            },
            '_pypi_ordering': 36,
            'classifiers': ['Framework :: Pyramid'],
            'name': 'pyramid_debugtoolbar',
            'bugtrack_url': None,
            'license': 'BSD',
            'summary': 'A package which provides an interactive HTML debugger for Pyramid application development',
            'home_page': 'http://docs.pylonsproject.org/projects/pyramid-debugtoolbar/en/latest/',
            'stable_version': None,
            'cheesecake_installability_id': None
        },
        'releases': {
            '1.0': [{
                'has_sig': False,
                'upload_time': '2012-03-17T22:43:08',
                'comment_text': '',
                'python_version': 'source',
                'url': 'https://pypi.python.org/packages/source/p/pyramid_debugtoolbar/pyramid_debugtoolbar-1.0.tar.gz',
                'md5_digest': '37bff0f1d44941b97137dab24facc978',
                'downloads': 6487,
                'filename': 'pyramid_debugtoolbar-1.0.tar.gz',
                'packagetype': 'sdist',
                'size': 1626279
            }],
        },
        'urls': [{
                'has_sig': False,
                'upload_time': '2015-01-05T21:45:08',
                'comment_text': '',
                'python_version': '2.7',
                'url': 'https://pypi.python.org/packages/2.7/p/pyramid_debugtoolbar/pyramid_debugtoolbar-2.3-py2.py3-none-any.whl',
                'md5_digest': '64e1cfcf6a988edb189af13e36ab875c',
                'downloads': 4425,
                'filename': 'pyramid_debugtoolbar-2.3-py2.py3-none-any.whl',
                'packagetype': 'bdist_wheel',
                'size': 449260
            },
            {
                'has_sig': False,
                'upload_time': '2015-01-05T21:44:32',
                'comment_text': '',
                'python_version': 'source',
                'url': 'https://pypi.python.org/packages/source/p/pyramid_debugtoolbar/pyramid_debugtoolbar-2.3.tar.gz',
                'md5_digest': '3d4c2af7d4f45efd796cdd58126ac446',
                'downloads': 9075,
                'filename': 'pyramid_debugtoolbar-2.3.tar.gz',
                'packagetype': 'sdist',
                'size': 3017109
            }]
        }
}


def pypi_app(environ, start_response):
    package_name = environ['PATH_INFO'].split('/')[2]

    if package_name in DB:
        data = json.dumps(DB[package_name])

        start_response('200 OK', [
            ('Content-Type', 'application/json; charset="UTF-8"'),
            ('Content-Length', str(len(data)))])
        return [data]

    package_name = package_name.lower().replace('-', '_')

    if package_name in DB:
        start_response('301 Moved Permanently', [
            ('Location', '/pypi/{}/json'.format(package_name)),
            ('Content-Length', '0')])
        return ['']

    start_response('404 Not Found', [
        ('Content-Length', '0')])
    return ['']
