import os

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.utils.datastructures import MultiValueDict


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

