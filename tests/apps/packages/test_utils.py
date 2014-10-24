import pytest
from mock import Mock

from django.utils.datastructures import MultiValueDict

from localshop.apps.packages.utils import parse_distutils_request

LOCALSHOP_FIELDS = (
    ("license", ["BSD"]),
    ("name", ["localshop"]),
    ("metadata_version", ["1.0"]),
    ("author", ["Michael van Tellingen"]),
    ("home_page", ["http://github.com/mvantellingen/localshop"]),
    (":action", ["submit"]),
    ("download_url", [None]),
    ("summary", ["A private pypi server including auto-mirroring of pypi."]),
    ("author_email", ["michaelvantellingen@gmail.com"]),
    ("version", ["0.1"]),
    ("platform", [None]),
    ("classifiers", [
        "Development Status :: 2 - Pre-Alpha",
        "'Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ]),
    ("description", [None]),
)


def get_raw_form_data(fields, crlf=False):
    if crlf:
        # Python >=2.7.9 and >=3.4.2
        # See http://bugs.python.org/issue10510
        nl = "\r\n"
    else:
        nl = "\n"
    boundary = nl + "----------------GHSKFJDLGDS7543FJKLFHRE75642756743254" + nl
    data = boundary
    for key, values in fields:
        for value in values:
            if value is None:
                value = "UNKNOWN"
            data += nl + 'Content-Disposition: form-data; name="%s"' % (key,)
            data += 2 * nl
            data += value
            data += boundary
    return data


@pytest.mark.parametrize("crlf", [True, False])
def test_register_post(crlf):
    request = Mock()
    request.body = get_raw_form_data(LOCALSHOP_FIELDS, crlf)
    request.FILES = MultiValueDict()
    parse_distutils_request(request)

    expected_post = MultiValueDict(LOCALSHOP_FIELDS)
    expected_files = MultiValueDict()

    assert request.POST == expected_post
    assert request.FILES == expected_files
