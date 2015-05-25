Contributing
############

Want to contribute with Localshop? Great! We really appreciate your help. But
before digging into your new fluffy-next-millionaine-feature code keep in mind
that you **MUST** follow this guide to get your pull requests approved.


Get started
===========

1. Fork the project and follow the installation instructions [#rf1]_.

2. Your code **MUST** contain tests. This is a requirement and no pull request
   will be approved if it lacks tests. Even if your're making a small bug fix
   we want to ensure that it will not introduce any another bug.

3. Help to keep the documentation up-to-date is really appreaciated. Always
   check if your're making changes that make the documentation obsolete and
   update it.

4. `Squash your commits`_ before making a pull request whenever possible. This
   will avoid history pollution with middle commits that breaks things. Your
   pull request should be a single commit with all your changes.

5. Open a `pull request`_. Usually, the target branch at the main repository
   will be ``develop``, but if your're sending a bugfix to avoid the extinction
   of human race, maybe you want to target the ``master`` branch.


.. tip::
   Use a meaningful and convincing pull request description. Feel free to `use
   emojis`_ to give us a clue of what kind changes your're making. The `Style
   guide`_ contains some of our preferred ones.


Running Tests
-------------

To run all tests, simply use `tox`::

    pip install tox

    tox  # use `tox -r` to rebuild the virtual environment


To run a specific test, pass the test module filename as an argument::

    tox tests/apps/packages/test_models.py


Style guide
===========

- Follow the `PEP8`_. Try to keep the line length to 79 but don't make it a 
  big a deal.
- Make sure that your code does not raises any Pylint errors or warnings.
- Always group the imports in 3 blocks: native libraries, third party libraries
  and project imports.
- Keep the import block alphabetically ordered. If you use Sublime Text, you
  can do this by selecting the import block and hitting ``F9``
- Avoid polluting the current namespace with lots of imports. If you find
  yourself in a situation of importing a lot of symbols from the same package,
  consider import the package itself.
    
  **Wrong way**:

  .. code-block:: python
  
     from django.core.exceptions import (ImproperlyConfigured, AppRegistryNotReady, FieldError, DisallowedHost,
                                         DisallowedRedirect, DjangoRuntimeWarning)
  
  **Preferred way**:

  .. code-block:: python
  
        from django.core import exceptions as djexc


Commit messages
---------------

- Limit the first line to 72 characters or less
- Always use English
- Consider starting the commit message with an applicable emoji:
    - |lipstick| ``:lipstick:`` when improving the format/structure of the code
    - |fire| ``:fire:`` when removing code or files
    - |bug| ``:bug:`` when fixing a bug
    - |beetle| ``:beetle:`` when fixing a bug
    - |book| ``:book:`` when writing docs
    - |green_heart| ``:green_heart:`` when fixing the CI build
    - |white_check_mark| ``:white_check_mark:`` when adding tests
    - |x| ``:x:`` when commiting code with failed tests
    - |arrow_up| ``:arrow_up:`` when upgrading dependencies
    - |arrow_down| ``:arrow_down:`` when downgrading dependencies


.. |lipstick| image:: http://www.tortue.me/emoji/lipstick.png
   :width: 20px
   :height: 20px
.. |fire| image:: http://www.tortue.me/emoji/fire.png
   :width: 20px
   :height: 20px
.. |bug| image:: http://www.tortue.me/emoji/bug.png
   :width: 20px
   :height: 20px
.. |beetle| image:: http://www.tortue.me/emoji/beetle.png
   :width: 20px
   :height: 20px
.. |book| image:: http://www.tortue.me/emoji/book.png
   :width: 20px
   :height: 20px
.. |green_heart| image:: http://www.tortue.me/emoji/green_heart.png
   :width: 20px
   :height: 20px
.. |white_check_mark| image:: http://www.tortue.me/emoji/white_check_mark.png
   :width: 20px
   :height: 20px
.. |x| image:: http://www.tortue.me/emoji/x.png
   :width: 20px
   :height: 20px
.. |arrow_up| image:: http://www.tortue.me/emoji/arrow_up.png
   :width: 20px
   :height: 20px
.. |arrow_down| image:: http://www.tortue.me/emoji/arrow_down.png
   :width: 20px
   :height: 20px

.. rubric:: Footnotes

.. [#rf1] :ref:`installation-instructions`

.. _`Squash your commits`: http://git-scm.com/book/en/v2/Git-Tools-Rewriting-History#Squashing-Commits
.. _`pull request`: https://help.github.com/articles/using-pull-requests/
.. _`use emojis`: http://www.emoji-cheat-sheet.com
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
