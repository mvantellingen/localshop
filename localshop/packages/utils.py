import inspect

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from django.utils.datastructures import MultiValueDict
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from localshop.conf import settings
from localshop.permissions.models import CIDR


class OverwriteStorage(FileSystemStorage):
    """
    Comes from http://www.djangosnippets.org/snippets/976/
    (even if it already exists in S3Storage for ages)

    See also Django #4339, which might add this functionality to core.
    """

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        if self.exists(name):
            self.delete(name)
        return name


def validate_client(func):
    """Only allow downloads from authenticted users or from remote ip's
    which are listed in `LOCALSHOP_ALLOWED_REMOTE_IPS`

    """
    if inspect.isclass(func) and issubclass(func, View):
        original_dispatch = func.dispatch

        # XXX: The csrf_exempt here is a hack, should only be on SimpleIndex
        @method_decorator(csrf_exempt)
        @method_decorator(validate_client)
        def dispatch(cls, request, *args, **kwargs):
            return original_dispatch(cls, request, *args, **kwargs)
        func.dispatch = dispatch
        return func

    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)

        if CIDR.objects.has_access(request.META['REMOTE_ADDR']):
            return func(request, *args, **kwargs)
        return HttpResponseForbidden('No permission')
    return _wrapper


def parse_distutils_request(request):
    """Parse the `request.raw_post_data` and return a `MultiValueDict`
    for the POST data and the FILES data.

    This method is taken from the chishop source.

    """
    raw_post_data = request.raw_post_data
    sep = raw_post_data.splitlines()[1]
    items = raw_post_data.split(sep)
    post_data = {}
    files = {}
    for part in filter(lambda e: not e.isspace(), items):
        item = part.splitlines()
        if len(item) < 2:
            continue
        header = item[1].replace("Content-Disposition: form-data; ", "")
        kvpairs = header.split(";")
        headers = {}
        for kvpair in kvpairs:
            if not kvpair:
                continue
            key, value = kvpair.split("=")
            headers[key] = value.strip('"')
        if "name" not in headers:
            continue
        content = part[len("\n".join(item[0:2])) + 2:len(part) - 1]
        if "filename" in headers:
            file = SimpleUploadedFile(headers["filename"], content,
                    content_type="application/gzip")
            files["distribution"] = [file]
        elif headers["name"] in post_data:
            post_data[headers["name"]].append(content)
        else:
            # Distutils sends UNKNOWN for empty fields (e.g platform)
            # [russell.sim@gmail.com]
            if content == 'UNKNOWN':
                post_data[headers["name"]] = [None]
            else:
                post_data[headers["name"]] = [content]

    return MultiValueDict(post_data), MultiValueDict(files)

