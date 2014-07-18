from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from localshop.apps.packages import models
from localshop.apps.permissions.utils import credentials_required

dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)


@csrf_exempt
@credentials_required
def handle_request(request):
    response = HttpResponse(mimetype='application/xml')
    response.write(dispatcher._marshaled_dispatch(request.body))
    return response


def search(query, operator):
    """Implement xmlrpc search command.

    This only searches through the mirrored and private packages

    """
    field_map = {
        'name': 'name__icontains',
        'summary': 'releases__summary__icontains',
    }

    query_filter = None
    for field, values in query.iteritems():
        for value in values:
            if field not in field_map:
                continue

            field_filter = Q(**{field_map[field]: value})
            if not query_filter:
                query_filter = field_filter
                continue

            if operator == 'and':
                query_filter &= field_filter
            else:
                query_filter |= field_filter

    result = []
    packages = models.Package.objects.filter(query_filter).all()[:20]
    for package in packages:
        release = package.releases.all()[0]
        result.append({
            'name': package.name,
            'summary': release.summary,
            'version': release.version,
            '_pypi_ordering': 0,
        })
    return result

dispatcher.register_function(search, 'search')
