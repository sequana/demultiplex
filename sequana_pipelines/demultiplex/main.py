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

                sequana_pipelines_demultiplex --bcl-directory PATH_TO_DATA --sample-sheet SampleSheet.csv


        """
        )
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        # add a new group of options to the parser
        # demultiplex requires lots of memory sometimes hence the 64G options
        # 
        so = SlurmOptions(queue="biomics", memory="64000", cores=16)
        so.add_options(self)

        # add a snakemake group of options to the parser
        so = SnakemakeOptions(working_directory="fastq")
        so.add_options(self)


        so = GeneralOptions()
        so.add_options(self)


        pipeline_group = self.add_argument_group("pipeline")

        pipeline_group.add_argument("--threads", dest="threads", default=4,
            type=int, help="Number of threads to use during the demultiplexing. ")
        pipeline_group.add_argument("--barcode-mismatch", dest="mismatch", default=0, type=int)
        pipeline_group.add_argument("--merging-strategy", required=True,
            dest="merging_strategy", choices=["merge", "none"], 
            help="""Merge Lanes of not. Set to 'merge' to merge all lanes. Set
            to 'none' to NOT merge the lanes""")
        pipeline_group.add_argument("--bcl-directory", dest="bcl_directory",
            required=True, help="""Directory towards the raw BCL files. This directory should
            contains files such as RunParameters.xml, RunInfo.xml """)
        pipeline_group.add_argument("--sample-sheet", dest="samplesheet",
            required=True,
            default="SampleSheet.csv", help="Sample sheet filename to be used")
        pipeline_group.add_argument("--ignore-missing-controls", 
            dest="ignore_missing_controls", action="store_true", default=True)
        pipeline_group.add_argument("--ignore-missing-bcls",
            dest="ignore_missing_bcls", action="store_true", default=True)
        pipeline_group.add_argument("--no-bgzf-compression",
            dest="no_bgzf_compression", action="store_true", default=True)
        pipeline_group.add_argument("--write-fastq-reverse-complement",
            dest="write_fastq_reverse_complement", action="store_true", default=True)


def main(args=None):

    if args is None:
        args = sys.argv

    if "--version" in sys.argv:
        print_version(NAME)
        sys.exit(0)

    options = Options(NAME).parse_args(args[1:])

    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters. First, let us check some input
    # files
    manager.exists(options.samplesheet)
    manager.exists(options.bcl_directory)

    runparam = options.bcl_directory + os.sep + "RunParameters.xml"
    manager.exists(runparam, warning_only=True)

    if os.path.exists(runparam):
        with open(runparam, "r") as fin:
            data = fin.read()
            if "NextSeq" in data and options.merging_strategy == "none":
                logger.warning("This looks like a NextSeq run. You set "
"merging_strategy to none. Most probably you want to merge the lanes. Use "
"'--merging-strategy merge' instead")


    cfg = manager.config.config
    cfg.input_directory = os.path.abspath(options.bcl_directory)
    cfg.bcl2fastq.threads = options.threads
    cfg.bcl2fastq.barcode_mismatch = options.mismatch
    cfg.bcl2fastq.sample_sheet_file = os.path.abspath(options.samplesheet)


    # this is defined by the working_directory
    cfg.bcl2fastq.output_directory = "."
    cfg.bcl2fastq.ignore_missing_controls= options.ignore_missing_controls
    cfg.bcl2fastq.ignore_missing_bcls = options.ignore_missing_bcls
    cfg.bcl2fastq.no_bgzf_compression = options.no_bgzf_compression
    if options.merging_strategy == "merge":
        cfg.bcl2fastq.merge_all_lanes = True
    elif options.merging_strategy == "none":
        cfg.bcl2fastq.merge_all_lanes = False
    cfg.bcl2fastq.write_fastq_reverse_complement = options.write_fastq_reverse_complement

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown()


if __name__ == "__main__":
    main()
