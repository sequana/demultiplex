:Overview: Performs the demultiplexing of your raw Illumina data
:Input: bcl files from an Illumina sequencer
:Output: fastq files

Usage
~~~~~~~

::

    sequana_pipelines_demultiplex --bcl-directory bcl --working-directory fastq --samplesheet SampleSheet.csv


Requirements
~~~~~~~~~~~~~~~~~~

This pipeline is to be used with bcl2fastq 2.20.0 and sequana>=0.8.0 

.. image:: https://raw.githubusercontent.com/sequana/sequana_demultiplex/master/sequana_demultiplex/sequana_pipelines/demultiplex/dag.png



Details
~~~~~~~

This pipeline uses the standard **bcl2fastq** tool from Illumina. You will have
to install yourself since it is not yet part of a distribution such as bioconda. 

We then create some plots to help the user to understand the results. We
indicate the rate of undetermined and missing index can easily be retrieved from
one of the output plot as well.

