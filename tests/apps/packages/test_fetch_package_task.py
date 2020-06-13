import pytest

from localshop.apps.packages.tasks import fetch_package
from tests.factories import PackageFactory, ReleaseFactory, RepositoryFactory


@pytest.mark.django_db
def test_fetch_package(pypi_stub):
    repository = RepositoryFactory(upstream_pypi_url=pypi_stub)
    fetch_package(repository.pk, 'minibar')

    package = repository.packages.filter(name='minibar').first()

    assert package
    assert package.name == 'minibar'
    assert not package.is_local
    assert package.releases.count() == 2

    release_1, release_2 = package.releases.all()

    assert release_1.author == 'Cesar Canassa'
    assert release_1.author_email == 'cesar@canassa.com'
    assert release_1.description == 'Minibar'
    assert release_1.download_url == 'UNKNOWN'
    assert release_1.home_page == 'https://github.com/canassa/minibar'
    assert release_1.license == 'MIT'
    assert release_1.metadata_version == '1.0'
    assert release_1.summary == 'Simple text progress bar library'
    assert release_1.version == '0.4.0'

    assert release_2.author == 'Cesar Canassa'
    assert release_2.author_email == 'cesar@canassa.com'
    assert release_2.description == 'Minibar'
    assert release_2.download_url == 'UNKNOWN'
    assert release_2.home_page == 'https://github.com/canassa/minibar'
    assert release_2.license == 'MIT'
    assert release_2.metadata_version == '1.0'
    assert release_2.summary == 'Simple text progress bar library'
    assert release_2.version == '0.1'

    assert release_1.files.count() == 2

    file_1, file_2 = release_1.files.all()

    assert file_1.size == 5844
    assert file_1.filetype == 'bdist_wheel'
    assert file_1.filename == 'minibar-0.4.0-py2.py3-none-any.whl'
    assert file_1.md5_digest == '0bbdf41e028a4e6c75dfbd59660b6328'
    assert file_1.python_version == '3.4'
    assert file_1.requires_python is None
    assert file_1.url == 'https://pypi.python.org/packages/6c/60/8554f591f2a5a830c06070397df765d2cce36277459f3cb4ff2c2fa08369/minibar-0.4.0-py2.py3-none-any.whl'  # noqa

    assert file_2.size == 3956
    assert file_2.filetype == 'sdist'
    assert file_2.filename == 'minibar-0.4.0.tar.gz'
    assert file_2.md5_digest == 'a3768a7f948871d8e47b146053265100'
    assert file_2.python_version == 'source'
    assert file_1.requires_python is None
    assert file_2.url == 'https://pypi.python.org/packages/57/f3/fecf00ba7ec1989aa55d98be1eccd26a9c38a9cbe3ec70487908a8749ba1/minibar-0.4.0.tar.gz'  # noqa

    assert release_2.files.count() == 1

    file_1 = release_2.files.first()

    assert file_1.size == 3461
    assert file_1.filetype == 'sdist'
    assert file_1.filename == 'minibar-0.1.tar.gz'
    assert file_1.md5_digest == 'c935bfa49cb49e4f97fb8e24371105d7'
    assert file_1.python_version == 'source'
    assert file_1.requires_python is None
    assert file_1.url == 'https://files.pythonhosted.org/packages/4e/c5/9275972ae0aff6a8102978b677290aae7e7ca1133bc0765b685cc2d5b1f1/minibar-0.1.tar.gz' # noqa


@pytest.mark.django_db
def test_fetch_package_with_wrong_case(pypi_stub):
    repository = RepositoryFactory(upstream_pypi_url=pypi_stub)
    fetch_package(repository.pk, 'Minibar')

    assert repository.packages.filter(name='minibar').first()


@pytest.mark.django_db
def test_fetch_package_with_wrong_separator(pypi_stub):
    repository = RepositoryFactory(upstream_pypi_url=pypi_stub)
    fetch_package(repository.pk, 'pyramid-debugtoolbar')

    assert repository.packages.filter(name='pyramid_debugtoolbar').first()


@pytest.mark.django_db
def test_fetch_package_with_inexistent_package(pypi_stub):
    repository = RepositoryFactory(upstream_pypi_url=pypi_stub)
    fetch_package(repository.pk, 'arcoiro')

    assert not repository.packages.filter(name='arcoiro').first()


@pytest.mark.django_db
def test_fetch_package_should_update_existing_package(pypi_stub):
    repository = RepositoryFactory(upstream_pypi_url=pypi_stub)
    package = PackageFactory(repository=repository, name='minibar', normalized_name='minibar')
    ReleaseFactory(package=package, version='0.1')
    ReleaseFactory(package=package, version='0.2')

    fetch_package(repository.pk, 'minibar')

    package = repository.packages.filter(name='minibar').first()

    assert package
    assert package.name == 'minibar'
    assert not package.is_local
    assert package.releases.count() == 3

    release_1, release_2, release_3 = package.releases.all()

    assert release_1.version == '0.4.0'
    assert release_2.version == '0.2'
    assert release_3.version == '0.1'

    assert release_3.author == 'Cesar Canassa'
    assert release_3.author_email == 'cesar@canassa.com'
    assert release_3.description == 'Minibar'
    assert release_3.download_url == 'UNKNOWN'
    assert release_3.home_page == 'https://github.com/canassa/minibar'
    assert release_3.license == 'MIT'
    assert release_3.metadata_version == '1.0'
    assert release_3.summary == 'Simple text progress bar library'
