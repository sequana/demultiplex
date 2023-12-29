
.. image:: https://badge.fury.io/py/sequana-demultiplex.svg
     :target: https://pypi.python.org/pypi/sequana_demultiplex

.. image:: https://github.com/sequana/demultiplex/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/demultiplex/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/sequana/demultiplex/badge.svg?branch=main
    :target: https://coveralls.io/github/sequana/demultiplex?branch=main

.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg
    :target: https://pypi.python.org/pypi/sequana
    :alt: Python 3.8 | 3.9 | 3.10

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
   :target: http://joss.theoj.org/papers/10.21105/joss.00352
   :alt: JOSS (journal of open source software) DOI

This is is the **demultiplex** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs bcl2fastq on raw BCL data and creates plots to ease the QC validation
:Input: A valid Illumina base calling directory and sample sheet file
:Output: An HTML report, a set of PNG files and the expected FastQ files
:Status: production
:Wiki: https://github.com/sequana/demultiplex/wiki
:Documentation: This README file, the Wiki from the github repository (link above) and https://sequana.readthedocs.io
:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

Intall the **sequana_demultiplex** package as follows::

    pip install sequana_demultiplex

Usage
~~~~~

::

    sequana_demultiplex --help
    sequana_demultiplex --working-directory DATAPATH --bcl-directory bcldata --sample-sheet SampleSheet.csv --merging-strategy merge

The --bcl-directory option indicates where to find your raw data, the sample-sheet
expects the SampleSheet to be compatible with IEM software. The --merging-strategy can
be set to *none* or *merge*. The *merge* option merges the lanes, which is
useful for e.g. NextSeq sequencers.

This creates a directory **fastq**. You just need to execute the pipeline::

    cd demultiplex
    sh demultiplex.sh  # for a local run

These commands launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the demultiplex.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s demultiplex.rules --cores 4 --stats stats.txt \
        --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/"


You may also use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ for a graphical interface.

Would you need to merge the lane, please add the --merging-strategy argument
followed by *merge*::

    sequana_demultiplex --bcl-directory bcl_data --merging-strategy merge --sample-sheet SampleSheet.csv


Requirements
~~~~~~~~~~~~

This pipeline requires the following third-party tool(s):

- bcl2fastq 2.20.0

This software has an end-user license agreement (EULA). Given the EULA details
of this software, it cannot be distributed according to ` Illumina license <https://support.illumina.com/content/dam/illumina-support/documents/downloads/software/bcl2fastq/bcl2fastq2-v2-20-eula.pdf>`_
Therefore, you should install it yourself. On cluster facility, you may ask to
your system administator. For instance::

    module load bcl2fastq/2.20.0

For the same reason you cannot find it on community such as bioconda or docker (aug 2020).

So, you will need to download the code yourself. The easiest is to download the
RPM from `Illumina
<https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software/downloads.html>`_
and accept the agreements. Install it using the RPM if you have a debian-like system::

    rpm install file.rpm

If you do not have a debian system, you can look at https://damona.readthedocs.io where we provide
a singularity recipes to build an image from your own  rpm. Recipes can be found
`here <https://github.com/cokelaer/damona/tree/master/damona/recipes/bcl2fastq>`_.


Details
~~~~~~~~~
.. image:: https://raw.githubusercontent.com/sequana/demultiplex/master/sequana_pipelines/demultiplex/dag.png

This pipeline runs bcl2fastq 2.20 and creates a set of diagnostics plots to help
deciphering common issues such as missing index and sample sheet errors.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/demultiplex/master/sequana_pipelines/demultiplex/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file.



Changelog
~~~~~~~~~

========= =======================================================================
Version   Description
========= =======================================================================
1.5.2     * rename requirements.txt into tools.txt; update __init__
1.5.1     * switch working directory to fastq instead of demultiplex(regression)
1.5.0     * Uses click and new sequana_pipetools, add multiqc
1.4.0     * Implement demultiplexing of single cell ATAC seq data with
            cellranger.
1.3.1     * use sequana_wrappers version in the config file
1.3.0     * use latest sequana-wrappers to benefit and graphivz apptainer
1.2.1     * Update CI action and use new sequana_pipetools v0.9.0
1.2.0     * stable release with cleanup of the setup and README
1.1.3     * add the --mars-seq option that fills the config automatically
1.1.2     * fix the none_and_force merging strategy option
1.1.1     * fix a regression bug
1.1.0     * Uses new sequana-wrappers repository
1.0.5     * Fix regression bug to cope with new snakemake API
          * Compatibility with sequanix GUI
1.0.4     * Better HTML report with updated images.
          * validate the SampleSheet when using sequana_demultiplex and/or the
            pipeline
          * Add error handler from sequana_pipetools
          * save all undetermined barcodes (not just first 20)
          * No changes to the UI
          * technically, the input_directory option is now in a section so that
            it can be used in Sequanix
1.0.3     * remove check_samplesheet and fix_samplesheet modules now in sequana
          * check sample sheet but do not fail. Instead, informing users that
            there is an error and suggest to use 'sequana samplesheet
            --quick-fix'
1.0.2     Use 'sequana samplesheet --check ' command instead of deprecated
          sequana_check_sample_sheet command
1.0.1     change some default behaviour:

          * write_fastq_reverse_complement is now set to False by default
            like bcl2fastq
          * The --no-bgzf-compression option is changed into
            --bgzf-compression. We do not want this option by default.
          * The --ignore-missing-bcls option is changed into
            --no-ignore-missing-bcls so as to ignore missing bcls by default
            keep this option as a flag and keep same behaviour
          * Fix HTML syntax
1.0.0     * stable version pinned on sequana libraries
0.9.11    * fix label in plot_summary,
          * add new plot to show reads per sample + undetermined
          * add two tools one to check the samplesheet called
            sequana_sample_sheet and one called sequana_fix_samplesheet. The
            former is now inside the pipeline as well and when creating the
            pipeline
          * set --write_reverse_complement to False by default
          * remove the --ignore-missing-control which is deprecated anyway
0.9.10    * implement the new option --from-project, add missing MANIFEST
0.9.9     * simplification of the pipeline to use sequana 0.8.4 to speed up
            the --help calls.
          * include a summary HTML report
0.9.8     * fix typos
0.9.7     * Use new release of sequana_pipetools
          * set matplotlib backend to agg
          * include a simple HTML report
0.9.6     * Handle different RunParameter.xml name (NextSeq vs HiSeq)
0.9.5     * Fix a regression bug due to new sequana release. We do not check
            the input file (fastq) since this is not a sequence analysis
            pipeline
          * Check whether it is a NextSeq run. If so, merging-strategy must be
            set to 'merge'. Can be bypassed using --force
0.9.4     * Check the presence of the bcl input directory and samplesheet.
          * More help in the --help message.
          * add  --sample-sheet option to replace --samplesheet option
          * Fix the schema file
          * Check for presence of RunParameters.xml and provide information
            if merging-stratgy is set to None whereas it is a NextSeq run
0.9.3     Fix regression bug
0.9.2     remove warning due to relative paths.
0.9.1     Make the merging options compulsory. Users must tell whether they
          want to merge the lanes or not. This avoid to do the merging or not
          whereas the inverse was expected.
0.8.6     Uses 64G/biomics queue and 16 cores on a SLURM scheduler
========= =======================================================================



Contribute & Code of Conduct
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To contribute to this project, please take a look at the
`Contributing Guidelines <https://github.com/sequana/sequana/blob/master/CONTRIBUTING.rst>`_ first. Please note that this project is released with a
`Code of Conduct <https://github.com/sequana/sequana/blob/master/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.
