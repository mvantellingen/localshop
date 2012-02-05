from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

from localshop.packages.models import Package, Release, ReleaseFile


@login_required
def frontpage(request):

    recent_local = (Release.objects
        .filter(package__is_local=True)
        .order_by('created')
        .all())

    recent_mirror = (ReleaseFile.objects
        .filter(release__package__is_local=False)
        .exclude(distribution='')
        .order_by('modified')
        .all())

    return TemplateResponse(request, 'frontpage.html', {
        'recent_local': recent_local,
        'recent_mirror': recent_mirror,
    })
