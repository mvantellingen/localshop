from setuptools import setup, find_packages


tests_require = [
]

install_requires = [
    'South',
    'Django>=1.3.1',
    'django-kombu==0.9.4',
    'eventlet>=0.9.15',
    'kombu>=1.5.1',
    'gunicorn>=0.13.4',
    'python-daemon>=1.6',
    'django-celery',
    'django-model-utils>=1.0',
    'requests>=0.10',
]

setup(
    name='localshop',
    version='0.1',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    license='BSD',
    include_package_data=True,
    entry_points="""
    [console_scripts]
    localshop = localshop.scripts.runner:main
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
