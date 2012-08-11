import urlparse

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


def clean_redirect_url(request, url, default='/'):
    """ Use default setting if redirect_to is empty else do a
    security check -- don't allow redirection to a different
    host.

    """
    netloc = urlparse.urlparse(url)[1]
    if not url or (netloc and netloc != request.get_host()):
        url = default
    return url
