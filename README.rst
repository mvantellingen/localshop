localshop
=========

A pypi server which automatically proxies and mirrors pypi packages based 
upon packages requested. It also supports the uploading of local (private) 
packages.

Note that this is currently really, really alpha :-)


Getting started
===============

Download and install localshop via the following command::

    pip install localshop

This should best be done in a new virtualenv. Now initialize your localshop 
environment by issuing the following command::

    localshop init
    localshop upgrade

And then start it via::

    localshop start http --daemon
    localshop start worker --daemon

The worker is required to do the mirroring of the pypi packages once they 
are needed.

Create an initial user via the following command::

    localshop manage createsuperuser 

You can now visit http://localhost:8900/ and view all the packages in your
localshop!

Now to allow servers to download packages from your localshop you have to
add the ip addresses to the localshop config file. This file is located
at ~/.localshop/localshop.conf.py  At the end of the file a list is 
defined with ip addresses which are allowed to download files.

Changing this setting requires a restart of the http server. This should be
manageable via the webinterace in future releases.

Restarting the http server is done as follow::

    localshop stop http
    localshop start http --daemon



How it works
============
Packages which are requested and are unknown are looked up on pypi via the 
xmlrpc interface.  At the moment the client downloads one of the files which
is not yet mirror'ed a 302 redirect is issued to the correct file (on pypi).  
At that point the worker starts downloading the package and stores it in 
~/.localshop/files so that the next time the package is request it is 
available within your own shop!


Uploading local/private packages
================================
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

