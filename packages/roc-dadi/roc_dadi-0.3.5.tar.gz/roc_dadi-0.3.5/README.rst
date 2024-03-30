DADI PLUGIN README
===================

INTRODUCTION
-------------

This directory contains the source files of the RPW DAta DIspatcher (DADI), a plugin used to handle data files read/write by the RPW operation and data pipeline (RODP).

DADI is not designed to be run as a stand-alone plugin, but with the RODP.

DADI is developed with and run under the POPPY framework.

CONTENT
--------

::

    roc/                    plugin source files
    .editorconfig           EditorConfig config file
    .gitignore              .gitignore file
    .gitlab-ci              config file for Gitlab-CI
    .pre-commit-config.yaml pre-commit config file
    bump_descriptor.py      Python script to synchronize roc/dadi/descriptor.json content with the pyproject.toml data
    MANIFEST.in             Required to build Python package distributions
    poetry.lock             Used by poetry package
    pyproject.toml          pyproject.toml file (PEP518)
    README.rst              present file
    setup.py                setup.py (required for editable mode)

HOWTO
------

How to install the plugin?
..........................

The plugin is designed to be installed and run inside a RODP instance.
However it can be installed manually, by entering:

.. code::

    python -m pip install /path_to_plugin

N.B. To install the plugin in editable mode, run the command:

.. code::

    python -m pip install -e /path_to_plugin

The editable mode can only used if the setup.py file exits. Use the dephell module to generate it from the pyproject.toml file (dephell deps convert).

How to release a new version of the plugin?
...........................................................

1. Update the version field in the :code:`pyproject.toml` file.

2. Make sure the :code:`poetry.lock` file is up-to-date running: :code:`poetry update --lock`. (Use :code:`pip install poetry -U` to install poetry.)

3. Update the descriptor file running the command: :code:`python bump_descriptor.py -m <message>`, where `<message>` must contain the change log for the new version.

4. Commit last changes in the `develop` branch of Git repository. Merge `develop` branch into `master`. Create a new tag "X.Y.Z" from `master` branch. Rebase `master` onto `develop`. Push `master`, `develop` and the new tag in the distant server.

How to call the plugin?
..........................

The plugin can only by called from a POPPy-like pipeline (e.g, RODP).

The main command is:

.. code::

    python manage.py dadi

.. note::

    * The :code:`manage.py` file is inside the pipeline root directory (depending of the pipeline installation the alias :code:`pop` can be also used).
    * The command below will return the help message by default if no sub-command is passed
