import sys
import os
import argparse

from sequana.pipelines_common import *
from sequana.snaketools import Module
from sequana import logger
logger.level = "INFO"

col = Colors()

NAME = "demultiplex"
m = Module(NAME)
m.is_executable()


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME):
        usage = col.purple(
            """This script prepares the sequana pipeline demultiplex layout to
            include the Snakemake pipeline and its configuration file ready to
            use.

            In practice, it copies the config file and the pipeline into a
            directory (demultiplex) together with an executable script

            For a local run, use :

                sequana_pipelines_demultiplex --input-directory PATH_TO_DATA --run-mode local

            For a run on a SLURM cluster:

                sequana_pipelines_demultiplex --input-directory PATH_TO_DATA --run-mode slurm

        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="")

        # add a new group of options to the parser
        so = SlurmOptions()
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory="fastq")
        so.add_options(self)


        so = GeneralOptions()
        so.add_options(self)


        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument("--threads", dest="threads", default=4, type=int)
        pipeline_group.add_argument("--barcode-mismatch", dest="mismatch", default=0, type=int)
        pipeline_group.add_argument("--merge", dest="merge", action="store_true")
        pipeline_group.add_argument("--bcl-directory", dest="bcl_directory")
        pipeline_group.add_argument("--output-directory",
            dest="output_directory", default="fastq",
            help="Where to save the FASTQ results (default fastq )",
        )
        pipeline_group.add_argument("--samplesheet", dest="samplesheet", 
            default="SampleSheet.csv")
        pipeline_group.add_argument("--ignore-missing-controls", 
            dest="ignore_missing_controls", action="store_true", default=True)
        pipeline_group.add_argument("--ignore-missing-bcls",
            dest="ignore_missing_bcls", action="store_true", default=True)
        pipeline_group.add_argument("--no-bgzf-compression",
            dest="no_bgzf_compression", action="store_true", default=True)
        pipeline_group.add_argument("--merge_all_lanes",
            dest="merge_all_lanes", action="store_true", default=True)
        pipeline_group.add_argument("--write-fastq-reverse-complement",
            dest="write_fastq_reverse_complement", action="store_true", default=True)


def main(args=None):

    if args is None:
        args = sys.argv

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters
    if os.path.exists(options.samplesheet) is False:
        raise IOError("Please provide an existing sample sheet file with --samplesheet")


    cfg = manager.config.config
    cfg.input_directory = os.path.abspath(options.bcl_directory)
    cfg.bcl2fastq.threads = options.threads
    cfg.bcl2fastq.barcode_mismatch = options.mismatch
    cfg.bcl2fastq.sample_sheet_file = os.path.abspath(options.samplesheet)

    if os.path.exists(options.samplesheet) is False:
        logger.error("Input Samplesheet {} not found. ".format(options.samplesheet))
        sys.exit(1)

    cfg.bcl2fastq.output_directory = options.output_directory
    cfg.bcl2fastq.ignore_missing_controls= options.ignore_missing_controls
    cfg.bcl2fastq.ignore_missing_bcls = options.ignore_missing_bcls
    cfg.bcl2fastq.no_bgzf_compression = options.no_bgzf_compression
    cfg.bcl2fastq.merge_all_lanes = options.merge_all_lanes
    cfg.bcl2fastq.write_fastq_reverse_complement = options.write_fastq_reverse_complement

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
