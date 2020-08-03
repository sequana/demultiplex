This is is the **demultiplex** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet

:Overview: Runs bcl2fastq on raw BCL data and creates plots to ease the QC validation
:Input: A valid Illumina base calling directory
:Output: a set of PNG files and the expected FastQ files
:Status: production
:Wiki: https://github.com/sequana/sequana_demultiplex/wiki
:Documentation: This README file, the Wiki from the github repository (link above) and https://sequana.readthedocs.io
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
    sequana_pipelines_demultiplex --working-directory DATAPATH --bcl-directory bcldata --samplesheet SampleSheet.csv

This creates a directory **fastq**. You just need to execute the pipeline::

    cd demultiplex
    sh demultiplex.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can retrieve the demultiplex.rules and config.yaml files and then execute the pipeline yourself with specific parameters::

    snakemake -s demultiplex.rules --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Would you need to merge the lane, please add the --merging-strategy argument
followed by *merge*::

    sequana_pipelines_demultiplex --bcl-directory bcl_data --merging-strategy merge


Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- bcl2fastq 2.20.0



**bcl2fastq** should be present in your path. Most facilities have the tools
installed. On cluster, modules provide the tool as well. If you do not have it,
we provide a singularity image, which can be download as follow::

    singularity pull bcl2fastq.img shub://cokelaer/ngstools:bcl2fastq

Then, just add a script called **bc2fastq** in your binary PATH with is
content::

    singularity run PATH_TO_image/bcl2fastq.img ${1+"$@"}

Details
~~~~~~~~~
.. image:: https://raw.githubusercontent.com/sequana/sequana_demultiplex/master/sequana_pipelines/demultiplex/dag.png

This pipeline runs bcl2fastq 2.20 and creates a set of diagnostics plots to help
deciphering common issues such as missing index and sample sheet errors. 


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_demultiplex/master/sequana_pipelines/demultiplex/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 



Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
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
========= ====================================================================

