import sys
import os
import argparse

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog

col = Colors()

NAME = "demultiplex"


class Options(argparse.ArgumentParser):
    def __init__(self, prog=NAME, epilog=None):
        usage = col.purple(sequana_prolog.format(**{"name": NAME}))
        super(Options, self).__init__(usage=usage, prog=prog, description="",
            epilog=epilog,
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
            dest="merging_strategy", choices=["merge", "none", "none_force"], 
            help="""Merge Lanes of not. options are : merge, none, none_and_force.
            The 'merge' choice merges all lanes. The 'none' choice do NOT merge the lanes. 
            For NextSeq runs, we should merge the lanes; if users demultiplex NextSeq 
            and set this option to none, an error is raised. If you still want to 
            skip the merging step, then set this option to 'none_and_force'""")
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

    #if "--version" in sys.argv:
    #    from sequana_pipetools.misc import print_version
    #    print_version(NAME)
    #    sys.exit(0)

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import init_pipeline
    init_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])

    from sequana.snaketools import Module
    m = Module(NAME)
    m.is_executable()

    from sequana import logger
    from sequana.pipelines_common import PipelineManager
    logger.level = "INFO"
    # the real stuff is here
    manager = PipelineManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()

    # fill the config file with input parameters. First, let us check some input
    # files
    manager.exists(options.samplesheet)
    manager.exists(options.bcl_directory)

    # NextSeq
    runparam_1 = options.bcl_directory + os.sep + "RunParameters.xml"

    # HiSeq
    runparam_2 = options.bcl_directory + os.sep + "runParameters.xml"

    if os.path.exists(runparam_1):
        runparam = runparam_1
    elif os.path.exists(runparam_2):
        runparam = runparam_2
    else:
        runparam = None
        logger.warning("RunParameters.xml or runParameters.xml file not found")

    manager.exists(runparam, warning_only=True)

    if runparam:
        with open(runparam, "r") as fin:
            data = fin.read()
            if "NextSeq" in data and options.merging_strategy != "merge":
                if options.merging_strategy == "none_and_force":
                    msg = "This is a NextSeq. You set the --merging-strategy to"
                    msg += " none_and_force. So, we proceed with no merging strategy"
                    logger.warning(msg)
                if options.merging_strategy == "none":
                    msg = "This is a NEXTSEQ run. You must set the "
                    msg += " --merging-strategy to 'merge'."
                    logger.warning(msg)
                    sys.exit(1)


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
    elif options.merging_strategy in  ["none", "none_and_force"]:
        cfg.bcl2fastq.merge_all_lanes = False
    cfg.bcl2fastq.write_fastq_reverse_complement = options.write_fastq_reverse_complement

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown(check_input_files=False)


if __name__ == "__main__":
    main()
