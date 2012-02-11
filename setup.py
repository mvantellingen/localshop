import os
import sys
from setuptools import setup, find_packages, Command


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
    'netaddr==0.7.6',
    'docutils==0.8.1',
]

readme = []
with open('README.rst', 'r') as fh:
    readme = fh.readlines()


class RunTests(Command):
    """From django-celery"""
    description = "Run the django test suite from the tests dir."
    user_options = []
    extra_env = {}
    extra_args = ['packages']

    def run(self):
        for env_name, env_value in self.extra_env.items():
            os.environ[env_name] = str(env_value)

        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "localshop")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = os.environ.get(
                        "DJANGO_SETTINGS_MODULE", "localshop.conf.server")
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        prev_argv = list(sys.argv)
        try:
            sys.argv = [__file__, "test"] + self.extra_args
            execute_manager(settings_mod, argv=sys.argv)
        finally:
            sys.argv = prev_argv

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='localshop',
    version='0.2.2',
    author='Michael van Tellingen',
    author_email='michaelvantellingen@gmail.com',
    url='http://github.com/mvantellingen/localshop',
    description='A private pypi server including auto-mirroring of pypi.',
    long_description='\n'.join(readme),
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    cmdclass={"test": RunTests},
    license='BSD',
    include_package_data=True,
    entry_points="""
    [console_scripts]
    localshop = localshop.scripts.runner:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
