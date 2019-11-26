=========================
Sequana Pipeline Template
=========================

This repository is a Cookiecutter template to build new Sequana pipeline.


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a new Sequana pipeline project as follows::

    cookiecutter https://github.com/sequana/sequana_pipeline_template.git

you will be asked some questions in particular the name of the package. Just
answer to the first question. Give a name for a pipeline that is not already
used in the https://github.com/sequana/ organisation. For instance, if you define the
name as *varseq*, it will create a directory called sequana_varseq with a structure
similar to ::

    ├── doc
    │   ├── conf.py
    │   ├── index.rst
    │   └── Makefile
    ├── README.rst
    ├── requirements.txt
    ├── sequana_pipelines
    │   └── varseq
    │       ├── config.yaml
    │       ├── varseq.rules
    │       ├── README.rst
    │       ├── requirements.txt
    │       └── schema.yaml
    ├── setup.cfg
    └── setup.py

You can then edit the README, requirements, and the pipeline itself stored in
sequana_pipelines/varseq in particular the *config.yaml* and *varseq.rules* files.


Some future features to be included:

* Create a repo and put it there.
* Add the repo to your Travis-CI_ account.
* Install the dev requirements into a virtualenv. (``pip install -r requirements_dev.txt``)
* Register_ your project with PyPI.
* Run the Travis CLI command `travis encrypt --add deploy.password` to encrypt your PyPI password in Travis config
  and activate automated deployment on PyPI when you push a new tag to master branch.
* Add the repo to your ReadTheDocs_ account + turn on the ReadTheDocs service hook.
* Release your package by pushing a new tag to master.
* Add a `requirements.txt` file that specifies the packages you will need for
  your project and their versions. For more info see the `pip docs for requirements files`_.
* Activate your project on `pyup.io`_.

.. _`pip docs for requirements files`: https://pip.pypa.io/en/stable/user_guide/#requirements-files
.. _Register: https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives
