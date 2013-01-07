from localshop.apps.packages.models import Package


def sidebar(request):
    if not request.user.is_authenticated():
        return {'sidebar': {}}
    sidebar_local = (Package.objects
        .filter(is_local=True)
        .order_by('name')
        .all())

    return {
        'sidebar': {
            'local': sidebar_local
        }
    }
