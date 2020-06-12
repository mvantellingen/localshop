localshop
=========

.. image:: https://img.shields.io/pypi/v/localshop.svg
    :target: https://pypi.python.org/pypi/localshop/
    :alt: Latest Version

.. image:: https://travis-ci.org/mvantellingen/localshop.svg?branch=master
    :target: https://travis-ci.org/mvantellingen/localshop

.. image:: http://codecov.io/github/mvantellingen/localshop/coverage.svg?branch=master
    :target: http://codecov.io/github/mvantellingen/localshop?branch=master


A PyPI server which automatically proxies and mirrors PyPI packages based
upon packages requested. It has support for multiple indexes and team based
access and also supports the uploading of local (private) packages.

The full documentation is available on `Read The Docs`_

.. _`Read The Docs`: http://localshop.readthedocs.org/



Getting started
---------------

When you want to host it on AWS with the Azure AD oauth2 server use:

    docker run \
        -e DATABASE_URL=postgresql://user:password@host/database
        -e SECRET_KEY=<secret-key-for-django>
        -e LOCALSHOP_FILE_STORAGE=storages.backends.s3boto.S3BotoStorage
        -e LOCALSHOP_FILE_BUCKET_NAME=<your-aws-s3-bucket>
        -e OAUTH2_PROVIDER=azuread-oauth2 \
        -e OAUTH2_APPLICATION_ID=<your-oauth2-app-id>
        -e OAUTH2_SECRET_KEY=<your-oauth2-secret-key>
        mvantellingen/localshop

If you want more flexibility you can load your custom settings file by mounting
a docker volume and creating a localshop.conf.py. This file will be loaded by
localshop at the end of the settings file.

    docker run \
        -e DATABASE_URL=postgresql://user:password@host/database
        -e SECRET_KEY=<secret-key-for-django>
        -v $(PWD)/config:/home/localshop/conf/
        mvantellingen/localshop
