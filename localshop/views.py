from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponseNotModified, \
     HttpResponse
from django.template.response import TemplateResponse


from localshop.packages.models import Release, ReleaseFile


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


def static_media(request, path, root=None):
    """
    Serve static files below a given point in the directory structure.
    """
    from django.utils.http import http_date
    from django.views.static import was_modified_since
    import mimetypes
    import os.path
    import posixpath
    import stat
    import urllib

    document_root = root or os.path.join(settings.PROJECT_ROOT, 'static')

    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        raise Http404("Directory indexes are not allowed here.")
    if not os.path.exists(fullpath):
        raise Http404('"%s" does not exist' % fullpath)
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]):
        return HttpResponseNotModified(mimetype=mimetype)
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, mimetype=mimetype)
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    response["Content-Length"] = len(contents)
    return response


