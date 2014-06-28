import inspect
import hashlib
import logging
import os
import xmlrpclib

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import FieldDoesNotExist
from django.db.models.fields.files import FileField
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict

logger = logging.getLogger(__name__)


def parse_distutils_request(request):
    """Parse the `request.raw_post_data` and update the request POST and FILES
    attributes .

    """
    lines = request.raw_post_data.splitlines()
    seperator = next(line for line in lines if line.startswith('----'))
    request.POST = QueryDict('', mutable=True)

    raw_post = request.raw_post_data.split(seperator)

    raw_lines = [line.lstrip() for line in raw_post if line.lstrip()]
    try:
        request._files = MultiValueDict()
    except Exception:
        pass

    for line in raw_lines:

        line_content = line.lstrip().split('\n', 1)
        header = line_content[0]
        content = line_content[1]

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


def md5_hash_file(fh):
    """Return the md5 hash of the given file-object"""
    md5 = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()
