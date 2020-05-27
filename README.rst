lib_csv
=======

|Pypi Status| |license| |maintenance|

|Build Status| |Codecov Status| |Better Code| |code climate| |code climate coverage| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2021.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/lib_csv.svg?branch=master
   :target: https://travis-ci.org/bitranox/lib_csv
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/lib-csv.svg
   :target: https://badge.fury.io/py/lib_csv
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/lib_csv/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/lib_csv
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_csv?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_csv
.. |snyk security| image:: https://snyk.io/test/github/bitranox/lib_csv/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_csv
.. |code climate| image:: https://api.codeclimate.com/v1/badges/7fa21a0ced3820c5faa9/maintainability
   :target: https://codeclimate.com/github/bitranox/lib_csv/maintainability
   :alt: Maintainability
.. |code climate coverage| image:: https://api.codeclimate.com/v1/badges/7fa21a0ced3820c5faa9/test_coverage
   :target: https://codeclimate.com/github/bitranox/lib_csv/test_coverage
   :alt: Code Coverage

functions to read and write csv files

this is for bitranox internal use, so there is no detailed documentation.

supports python 3.5-3.8, pypy3 and possibly other dialects.

`100% code coverage <https://codecov.io/gh/bitranox/lib_csv>`_, mypy static type checking, tested under `Linux, macOS, Windows and Wine <https://travis-ci
.org/bitranox/lib_csv>`_, automatic daily builds  and monitoring

----

- `Installation and Upgrade`_
- `Usage`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_csv/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_csv/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_csv/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Installation and Upgrade
------------------------

From source code:

.. code-block:: bash

    # normal install
    python3 setup.py install
    # test without installing
    python3 setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    python3 -m pip install --upgrade lib_csv

    # test without installing
    python3 -m pip install lib_csv --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    python3 -m pip install --upgrade git+https://github.com/bitranox/lib_csv.git --upgrade-strategy eager
    # normal install
    python3 -m pip install --upgrade git+https://github.com/bitranox/lib_csv.git
    # test without installing
    python3 -m pip install git+https://github.com/bitranox/lib_csv.git --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi (if any):
    lib_csv
    # for the latest Development Version :
    lib_csv @ git+https://github.com/bitranox/lib_csv.git


    # to install and upgrade all modules mentioned in requirements.txt:
    python3 -m pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python3 -m pip install --upgrade lib_csv

    # for the latest Development Version
    python3 -m pip install --upgrade git+https://github.com/bitranox/lib_csv.git


via makefile:

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_csv.git
    $ cd lib_csv

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

    # ti install development environment
    $ make develop

Usage
-----------

.. code-block::

    import the module and check the code - its easy and documented there, including doctest examples.
    in case of any questions the usage section might be expanded at a later time

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    docopt

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"
- more test

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_csv/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

0.1.0
-----
2020-05-27:
    - new build matrix
    - mypy strict type testing
    - fix title in pypi documentation
    - drop python2.7 - python 3.4 support

0.0.1
-----
2020-05-06:
    - Initial public release

