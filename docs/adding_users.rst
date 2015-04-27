Adding users
============

You can add users using the Django admin backend at ``/admin``. In order for the
user to be able to generate credentials for his account, he needs the following
four user permissions:

* ``permissions.add_credential``
* ``permissions.change_credential``
* ``permissions.delete_credential``
* ``permissions.view_credential``
