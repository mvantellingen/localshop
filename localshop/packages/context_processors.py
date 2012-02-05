from localshop.packages.models import Package, Release, ReleaseFile


def sidebar(request):
    sidebar_local = (Package.objects
        .filter(is_local=True)
        .order_by('name')
        .all())

    return {
        'sidebar': {
            'local': sidebar_local
        }
    }

