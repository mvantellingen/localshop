from setuptools import setup, find_packages

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()

tests_require = [
    'pytest>=2.6.0',
    'pytest-cov>=1.7.0',
    'pytest-django>=2.8.0',
    'pytest-cache==1.0',
    'django-webtest==1.9.2',
    'factory-boy==2.5.2',
    'mock==1.0.1',
]


setup(
    name='localshop',
    version='0.10.0.dev',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/localshop/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'Django==1.11.7',
        'Pillow==3.4.2',
        'celery==4.1.0',
        'django-braces==1.11.0',
        'django-celery-beat==1.1.0',
        'django-celery-results==1.0.1',
        'django-configurations==2.0',
        'django-environ==0.4.4',
        'django-model-utils==3.0.0',
        'django-storages==1.6.5',
        'django-widget-tweaks==1.4.1',
        'docutils==0.12',
        'gunicorn==19.1.1',
        'netaddr==0.7.12',
        'requests==2.18.4',
        'sqlparse==0.1.15',
        'whitenoise==3.3.1',
        'Versio==0.3.0',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
