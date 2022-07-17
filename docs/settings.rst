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

If set to ``False``, users will be prevented from overwriting already existing
release files. Can be used to encourage developers to bump versions rather than
overwriting. This is PyPI's behaviour.

``LOCALSHOP_VERSIONING_TYPE``
-------------------------------

:default: ``None``

If set to ``False``, no versioning "style" will be enforced.

If you want to validated versions you can choose any `Versio <https://pypi.python.org/pypi/Versio>`_ available backends.

**IMPORTANT** the value of this config must be a full path of the wanted class e.g. `versio.version_scheme.Pep440VersionScheme`.

- **Simple3VersionScheme** which supports 3 numerical part versions (A.B.C
  where A, B, and C are integers)
- **Simple4VersionScheme** which supports 4 numerical part versions (A.B.C.D
  where A, B, C, and D are integers)
- **Pep440VersionScheme** which supports `PEP 440 <http://www.python.org/dev/peps/pep-0440/>`_ 
  versions (N[.N]+[{a|b|c|rc}N][.postN][.- devN][+local])
- **PerlVersionScheme** which supports 2 numerical part versions where the 
  second part is at least two digits A.BB where A and B - are integers and B is 
  zero padded on the left. For example: 1.02, 1.34, 1.567)
