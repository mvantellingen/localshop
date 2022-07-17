How it works
============

Packages which are requested and are unknown are looked up on pypi via the
xmlrpc interface.  At the moment the client downloads one of the files which
is not yet mirror'ed a 302 redirect is issued to the correct file (on pypi).
At that point the worker starts downloading the package and stores it in
~/.localshop/files so that the next time the package is request it is
available within your own shop!


Uploading local/private packages
--------------------------------

To upload your own packages to your shop you need to modify/create a .pypirc
file.  See the following example:

.. code-block:: ini

    [distutils]
    index-servers =
        local

    [local]
    username: myusername
    password: mysecret
    repository: http://localhost:8000/repo/default/

To upload a custom package issue the following command in your package::

    python setup.py upload -r local

It should now be available via the webinterace


Using the shop for package installation
---------------------------------------

To install packages with pip from your localshop add `-i` flag, e.g.::

    pip install -i http://localhost:8000/repo/default/ localshop

or edit/create a ~/.pip/pip.conf file following this template:

.. code-block:: ini

    [global]
    index-url = http://<access_key>:<secret_key>@localhost:8000/repo/default/

Then just use pip install as you are used to do.
You can replace access_key and secret_key by a valid username and password.

Credentials for authentication
------------------------------

If you don't want to use your Django username/password to authenticate
uploads and downloads you can easily create one of the random credentials
localshop can create for you.

Go to the Credentials section and click on create. Use the access key
as the username and the secret key as the password when uploading packages.
A ``~/.pypirc`` could look like this:

.. code-block:: ini

    [distutils]
    index-servers =
        local

    [local]
    username: 4baf221849c84a20b77a6f2d539c3e8a
    password: 200984e70f0c463b994388c4da26ec3f
    repository: http://localhost:8000/simple/

pip allows you do use those values in the index URL during download, e.g.::

    pip install -i http://<access_key>:<secret_key>@localhost:8000/repo/default/ localshop

So for example::

    pip install -i http://4baf221849c84a20b77a6f2d539c3e8a:200984e70f0c463b994388c4da26ec3f@localhost:8000/repo/default/ localshop

.. warning::

    Please be aware that those credentials are transmitted unencrypted over
    http unless you setup your localshop instance to run on a server that
    serves pages via https.

In case you ever think a credential has been compromised you can disable it
or delete it on the credential page.
