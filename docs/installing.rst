.. _installation-instructions:

Installing
==========

Download and install localshop via the following command::

    pip install localshop

This should best be done in a new virtualenv. Now initialize your localshop
environment by issuing the following command::

    localshop init

If you are upgrading from an earlier version simply run::

    localshop upgrade

And then start it via::

    gunicorn localshop.wsgi:application

You will also need to start the celery daemon, it's responsible for downloading
and updating the packages from PyPI. So open another terminal, activate your
virtualenv (if you have created one) and run the following command::

    localshop celery worker -B -E

You can now visit http://localhost:8000/ and view all the packages in your
localshop!

**Note:** If you prefer to start listening on a different network interface and
HTTP port, you have the pass the parameter ``-b`` to ``gunicorn``. For example,
the following command starts localshop on port 7000 instead of 8000::

    gunicorn localshop.wsgi:application -b 0.0.0.0:7000

The next step is to give access to various hosts to use the shop. This is done
via the webinterface (menu -> permissions -> cidr). Each ip address listed there
will be able to download and upload packages. If you are unsure about ips
configuration, but still want to use authentication, specify "0.0.0.0/0" as the
unique cidr configuration. It will enable for any ip address.


Docker alternative
------------------
Install docker and docker-compose and then run:

.. code-block:: bash

    cp docker.conf.py{.example,}
    docker-compose build
    docker-compose run worker syncdb
    docker-compose run worker createsuperuser
    docker-compose up

You should be able to see localshop running in `http://docker-host:8000`.
