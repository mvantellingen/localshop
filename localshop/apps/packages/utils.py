import hashlib
import importlib
import logging
import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import FieldDoesNotExist
from django.db.models.fields.files import FileField
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

logger = logging.getLogger(__name__)


def parse_distutils_request(request):
    """
    Due to a bug in the Python distutils library, the request post is sent using \n
    as a separator instead of the \r\n that the HTTP spec demands. This breaks the Django
    form parser and therefore we have to write a custom parser.

    This bug was fixed in the Python 2.7.4 and 3.4:

    http://bugs.python.org/issue10510
    """
    if not request.body.endswith('\r\n'):
        sep = request.body.splitlines()[1]

        request.POST = QueryDict('', mutable=True)
        try:
            request._files = MultiValueDict()
        except Exception:
            pass

        for part in filter(lambda e: e.strip(), request.body.split(sep)):
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
                request.POST.appendlist(headers["name"], content)
    else:
        request.FILES['distribution'] = request.FILES['content']

    # Distutils sends UNKNOWN for empty fields (e.g platform)
    for key, value in request.POST.items():
        if value == 'UNKNOWN':
            request.POST[key] = None


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


def md5_hash_file(fh):
    """Return the md5 hash of the given file-object"""
    md5 = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def get_versio_versioning_scheme(full_class_path):
    """Return a class based on it's full path"""
    module_path = '.'.join(full_class_path.split('.')[0:-1])
    class_name = full_class_path.split('.')[-1]
    try:
        module = importlib.import_module(module_path)
    except ImportError:
        raise RuntimeError('Invalid specified Versio schema {}'.format(full_class_path))

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise RuntimeError('Could not find Versio schema class {!r} inside {!r} module.'.format(class_name, module_path))
