from setuptools import find_packages, setup

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()

tests_require = [
    'django-webtest==1.9.7',
    'factory-boy==2.12.0',
    'mock==4.0.2',
    'pytest-cov==2.8.1',
    'pytest-django==3.9.0',
    'pytest==5.4.2',
    'requests-mock==1.8.0',
    'requests-toolbelt==0.9.1',
]

setup(
    name='localshop',
    version='2.0.0-alpha.1',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    zip_safe=False,
    install_requires=[
        'boto3==1.14.1',
        'celery==4.4.0',
        'django-braces==1.14.0',
        'django-celery-beat==2.0.0',
        'django-celery-results==1.2.1',
        'django-environ==0.4.5',
        'django-model-utils==4.0.0',
        'django-storages==1.9.1',
        'django-widget-tweaks==1.4.8',
        'Django==2.2.13',
        'docutils==0.16',
        'netaddr==0.7.19',
        'Pillow==7.1.2',
        'psycopg2-binary==2.8.5',
        'redis==3.5.3',
        'requests==2.23.0',
        'social-auth-app-django==3.4.0',
        'sqlparse==0.3.1',
        'Versio==0.4.0',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    license='BSD',
    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages('src'),
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
