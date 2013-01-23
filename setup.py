import os
import sys
from setuptools import setup, find_packages, Command


install_requires = [
    'Django==1.4.3',
    'South==0.7.6',
    'Pillow==1.7.7',
    'celery==3.0.12',
    'kombu==2.5.4',
    'django-celery==3.0.11',
    'django-model-utils==1.1.0',
    'django-userena==1.1.2',
    'django-uuidfield==0.4.0',
    'django-storages==1.1.5',
    'django-configurations==0.1',
    'docutils==0.10',
    'eventlet==0.10.0',
    'gunicorn==0.17.1',
    'netaddr==0.7.10',
    'requests==1.0.4',
]

tests_requires = [
    'mock',
    'django-nose==1.1',
    'factory-boy==1.2.0',
]

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()


class RunTests(Command):
    """From django-celery"""
    description = "Run the django test suite from the tests dir."
    user_options = []
    extra_env = {}

    def run(self):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(
                self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, 'localshop')
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)

        os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get(
            'DJANGO_SETTINGS_MODULE', 'localshop.settings')
        os.environ['DJANGO_CONFIGURATION'] = os.environ.get(
            'DJANGO_CONFIGURATION', 'Localshop')

        from configurations.management import execute_from_command_line
        execute_from_command_line([__file__, 'test'])

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='localshop',
    version='0.4.1',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require={'test': tests_requires},
    cmdclass={"test": RunTests},
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
    ],
)
