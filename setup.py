import os
import sys
import re
from setuptools import setup, find_packages, Command


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        elif re.match(r'\s*-r\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links


readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()


setup(
    name='localshop',
    version='0.8.3',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django==1.7.1',
        'Pillow==2.6.1',
        'celery==3.1.17',
        'kombu==3.0.24',
        'django-celery==3.1.16',
        'django-model-utils==2.2.0',
        'django-userena==1.3.1',
        'django-uuidfield==0.5.0',
        'django-storages==1.1.8',
        'django-configurations==0.8',
        'django-environ==0.3.0',
        'docutils==0.11',
        'netaddr==0.7.12',
        'requests==2.5.1',
    ],
    extras_require={
        'mysql': ['mysqlclient==1.3.6'],
        'postgresql': ['psycopg2==2.6'],
        'gunicorn': ['gunicorn==19.1.1'],
        'redis': ['celery[redis]==3.1.17'],
    },
    license='BSD',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'localshop = localshop.runner:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
)
