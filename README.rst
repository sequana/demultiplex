This is is the **demultiplex** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs bcl2fastq on raw BCL data and create some QC plots to ease the QC step
:Input: A valid Illumina base calling directory
:Output: a set of PNG files and the expected FastQ files
:Status: production
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_demultiplex

Usage
~~~~~

::

    sequana_pipelines_demultiplex --help
    sequana_pipelines_demultiplex --working-directory DATAPATH --bcl-directory bcldata

This creates a directory **fastq**. You just need to execute the pipeline::

    cd demutliplex
    sh demutliplex.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the demutliplex.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s demutliplex.rules --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- bcl2fastq 2.20.0


.. image:: https://raw.githubusercontent.com/sequana/sequana_demulitiplex/master/sequana_pipelines/demultiplex/dag.png


Details
~~~~~~~~~

This pipeline runs bcl2fastq 2.20 and creates a set of diagnostics plots to help
deciphering common issues such as missing index and sample sheet errors. 



Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_demutliplex/master/sequana_pipelines/demutliplex/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

