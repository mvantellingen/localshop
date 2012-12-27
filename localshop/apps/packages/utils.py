import inspect
import logging
import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import FieldDoesNotExist
from django.db.models.fields.files import FileField
from django.http import QueryDict, HttpResponseForbidden
from django.utils.datastructures import MultiValueDict
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt

from localshop.apps.permissions.models import CIDR
from localshop.apps.permissions.utils import credentials_required

logger = logging.getLogger(__name__)


def validate_client(func):
    """
    Only allow downloads from authenticted users or from remote ip's
    that match one of the ones in the CIDR database.
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
        if CIDR.objects.has_access(request.META['REMOTE_ADDR']):
            return func(request, *args, **kwargs)
        return HttpResponseForbidden('No permission')

    return credentials_required(_wrapper)


def parse_distutils_request(request):
    """Parse the `request.raw_post_data` and update the request POST and FILES
    attributes .

    """

    try:
        sep = request.raw_post_data.splitlines()[1]
    except:
        raise ValueError('Invalid post data')

    request.POST = QueryDict('', mutable=True)
    try:
        request._files = MultiValueDict()
    except Exception:
        pass

    for part in filter(lambda e: e.strip(), request.raw_post_data.split(sep)):
        try:
            header, content = part.lstrip().split('\n', 1)
        except Exception:
            continue

        if content.startswith('\n'):
            content = content[1:]

        if content.endswith('\n'):
            content = content[:-1]

        headers = parse_header(header)

        if "name" not in headers:
            continue

        if "filename" in headers and headers['name'] == 'content':
            dist = TemporaryUploadedFile(name=headers["filename"],
                                         size=len(content),
                                         content_type="application/gzip",
                                         charset='utf-8')
            dist.write(content)
            dist.seek(0)
            request.FILES.appendlist('distribution', dist)
        else:
            # Distutils sends UNKNOWN for empty fields (e.g platform)
            # [russell.sim@gmail.com]
            if content == 'UNKNOWN':
                content = None
            request.POST.appendlist(headers["name"], content)


def parse_header(header):
    headers = {}
    for kvpair in filter(lambda p: p,
                         map(lambda p: p.strip(),
                             header.split(';'))):
        try:
            key, value = kvpair.split("=", 1)
        except ValueError:
            continue
        headers[key.strip()] = value.strip('"')

    return headers


def delete_files(sender, **kwargs):
    """Signal callback for deleting old files when database item is deleted"""
    for fieldname in sender._meta.get_all_field_names():
        try:
            field = sender._meta.get_field(fieldname)
        except FieldDoesNotExist:
            continue

        if isinstance(field, FileField):
            instance = kwargs['instance']
            fieldfile = getattr(instance, fieldname)

            if not hasattr(fieldfile, 'path'):
                return

            if not os.path.exists(fieldfile.path):
                return

            # Check if there are other instances which reference this fle
            is_referenced = (
                instance.__class__._default_manager
                .filter(**{'%s__exact' % fieldname: fieldfile})
                .exclude(pk=instance._get_pk_val())
                .exists())
            if is_referenced:
                return

            try:
                field.storage.delete(fieldfile.path)
            except Exception:
                logger.exception(
                    'Error when trying to delete file %s of package %s:' % (
                        instance.pk, fieldfile.path))
