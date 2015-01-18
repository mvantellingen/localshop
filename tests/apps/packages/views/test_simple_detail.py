import pytest

from django.core.urlresolvers import reverse

from localshop.apps.permissions.models import CIDR
from tests.apps.packages.factories import ReleaseFileFactory


@pytest.mark.django_db
def test_simple_detail_success(client, admin_user):
    CIDR.objects.create(cidr='0.0.0.0/0', require_credentials=False)
    release_file = ReleaseFileFactory()

    response = client.get(reverse('packages-simple:simple_detail', kwargs={
        'slug': release_file.release.package.name,
        'version': '',
    }))

    assert response.status_code == 200
    assert 'Links for test-package' in response.content
    assert ('<a href="/packages/test-package/download/1/test-1.0.0-sdist.zip'
            '#md5=62ecd3ee980023db87945470aa2b347b" rel="package">'
            'test-1.0.0-sdist.zip</a>') in response.content
