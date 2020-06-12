from localshop.apps.packages import pypi


def test_get_package_information(pypi_stub):
    assert pypi.get_package_information(pypi_stub, 'minibar')
