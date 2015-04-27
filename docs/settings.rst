Settings
========

There are a few settings to set in ``~/.localshop/localshop.conf.py`` that
change the behaviour of the localshop.

``LOCALSHOP_DELETE_FILES``
--------------------------

:default: ``False``

If set to ``True`` files will be cleaned up after deleting a package or
release from the localshop.

``LOCALSHOP_DISTRIBUTION_STORAGE``
----------------------------------

:default: ``'storages.backends.overwrite.OverwriteStorage'``

The dotted import path of a Django storage class to be used when uploading
a release file or retrieving it from PyPI.

``LOCALSHOP_HTTP_PROXY``
------------------------

:default: ``None``

Proxy configuration used for Internet access. Expects a dictionary configured
as mentioned by
http://docs.python-requests.org/en/latest/user/advanced/#proxies

``LOCALSHOP_ISOLATED``
----------------------

:default: ``False``

If set to ``True`` Localshop never will try to redirect the client to PyPI.
This is useful for environments where the client has no Internet connection.

.. note::
   If you set ``LOCALSHOP_ISOLATED`` to ``True``, client request can be delayed
   for a long time because the package must be downloaded from Internet before
   it is served. You may want to set pip environment variable
   ``PIP_DEFAULT_TIMEOUT`` to a big value. Ex: ``300``

``LOCALSHOP_USE_PROXIED_IP``
----------------------------

:default: ``False``

If set to ``True`` Localshop will use the X-Forwarded-For header to validate
the client IP address. Use this when Localshop is running behind a reverse
proxy such as Nginx or Apache and you want to use IP-based permissions.

``LOCALSHOP_RELEASE_OVERWRITE``
-------------------------------

:default: ``True``

If set to ``False``, users will be preveneted from overwriting already existing
release files. Can be used to encourage developers to bump versions rather than
overwriting. This is PyPI's behaviour.
