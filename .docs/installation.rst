From source code:

.. code-block:: bash

    # normal install
    python3 setup.py install
    # test without installing
    python3 setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    python3 -m pip install --upgrade {repository}

    # test without installing
    python3 -m pip install {repository} --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    python3 -m pip install --upgrade git+https://github.com/{repository_slug}.git --upgrade-strategy eager
    # normal install
    python3 -m pip install --upgrade git+https://github.com/{repository_slug}.git
    # test without installing
    python3 -m pip install git+https://github.com/{repository_slug}.git --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi (if any):
    {repository}
    # for the latest Development Version :
    {repository} @ git+https://github.com/{repository_slug}.git


    # to install and upgrade all modules mentioned in requirements.txt:
    python3 -m pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python3 -m pip install --upgrade {repository}

    # for the latest Development Version
    python3 -m pip install --upgrade git+https://github.com/{repository_slug}.git


via makefile:

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/{repository_slug}.git
    $ cd {repository}

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
