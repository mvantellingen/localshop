from setuptools import setup, find_packages

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()

tests_require = [
    'pytest>=2.6.0',
    'pytest-cov>=1.7.0',
    'pytest-django>=2.8.0',
    'pytest-cache==1.0',
    'django-webtest==1.7.8',
    'factory-boy==2.5.2',
    'mock==1.0.1',
]


setup(
    name='localshop',
    version='0.10.0.dev',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django>=1.8,<1.9',
        'celery>3.1,<3.2',
        'kombu>=3.0.26,<3.1',
        'django-braces>=1.8.0,<2.0',
        'django-cache-url',
        'django-celery>=3.1.16,<3.2',
        'django-configurations>=2.0,<2.1',
        'django-model-utils>=2.2,<2.7',
        'django-uuidfield==0.5.0',
        'django-storages-redux>=1.2.3,<1.4',
        'django-widget-tweaks>=1.3,<1.5',
        'dj-database-url',
        'dj-email-url',
        'docutils==0.12',  # used in apps.packages
        'netaddr>=0.7.12,<0.8',
        'requests>=2.7,<2.12',
        'whitenoise>=3.2,<3.3',
        'Versio>=0.2.1',
    ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
