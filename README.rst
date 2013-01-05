localshop
=========

.. image:: https://secure.travis-ci.org/mvantellingen/localshop.png?branch=develop

A pypi server which automatically proxies and mirrors pypi packages based 
upon packages requested. It also supports the uploading of local (private) 
packages.

Getting started
---------------

Download and install localshop via the following command::

    pip install localshop

This should best be done in a new virtualenv. Now initialize your localshop 
environment by issuing the following command::

    localshop init

If you are upgrading from an earlier version simply run::

    localshop upgrade

And then start it via::

    localshop run_gunicorn
    localshop celeryd -B -E

Celeryd is required to do the mirroring of the pypi packages once they 
are needed.

You can also start it via honcho using the Procfile::

    pip install -r honcho
    honcho start

You can now visit http://localhost:8000/ and view all the packages in your
localshop!

The next step is to give access to various hosts to use the shop. This
is done via the webinterface (menu -> permissions -> cidr). Each ip
address listed there will be able to download and upload packages.


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
file.  See the following example::

    [distutils]
    index-servers =
        local

    [local]
    username: myusername
    password: mysecret
    repository: http://localhost:8900/simple/

To upload a custom package issue the following command in your package::
    
    python setup.py upload -r local

It should now be available via the webinterace


Using the shop for package installation
=======================================

To install packages with pip from your localshop add `-i` flag, e.g.::
    
    pip install -i http://localhost:8900/simple/ localshop

Credentials for authentication
------------------------------

If you don't want to use your Django username/password to authenticate
uploads and downloads you can easily create one of the random credentials
localshop can create for you.

Go to the Credentials section and click on create. Use the access key
as the username and the secret key as the password when uloading packages.
A ``.pypirc`` could look like this::

    [distutils]
    index-servers =
        local

    [local]
    username: 4baf221849c84a20b77a6f2d539c3e8a
    password: 200984e70f0c463b994388c4da26ec3f
    repository: http://localhost:8900/simple/

pip allows you do use those values in the index URL during download, e.g.::

    pip install -i http://<access_key>:<secret_key>@localhost:8900/simple/ localshop

So for example::

    pip install -i http://4baf221849c84a20b77a6f2d539c3e8a:200984e70f0c463b994388c4da26ec3f@localhost:8900/simple/ localshop

.. warning::

    Please be aware that those credentials are transmitted unencrypted over
    http unless you setup your localshop instance to run on a server that
    serves pages via https.

In case you ever think a credential has been compromised you can disable it
or delete it on the credential page.

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
