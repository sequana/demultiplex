#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import sys
import os
import argparse
import subprocess

from sequana_pipetools.options import *
from sequana_pipetools.misc import Colors
from sequana_pipetools.info import sequana_epilog, sequana_prolog
from sequana_pipetools import SequanaManager

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
            dest="merging_strategy", choices=["merge", "none", "none_and_force"],
            help="""Merge Lanes or not. options are : merge, none, none_and_force.
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
        pipeline_group.add_argument("--no-ignore-missing-bcls",
            dest="no_ignore_missing_bcls", action="store_true", default=False,
            help="""In bcl2fastq, the option --ignore-missing-bcls implies that
we assume 'N'/'#' for missing calls. In Sequana_demultiplex, we use that option
by default. If you do not want that behviour, but the one from bcl2fastq, use
this flag(--no-ignore-missing-bcls)""")
        pipeline_group.add_argument("--bgzf-compression",
            dest="bgzf_compression", action="store_true", default=False,
            help="""turn on BGZF compression for FASTQ files. By default,
bcl2fastq uses this option; By default we don't. Set --bgzl--compression flag to
set it back""")
        self.add_argument("--mars-seq", default=False, action="store_true",
            help="""Set options to  --minimum-trimmed-read-length 15 --mask-short-adapter-reads 15 
and do not merge lanes""")
        self.add_argument("--run", default=False, action="store_true",
            help="execute the pipeline directly")

    def parse_args(self, *args):
        args_list = list(*args)
        if "--from-project" in args_list:
            if len(args_list)>2:
                msg = "WARNING [sequana]: With --from-project option, " + \
                        "pipeline and data-related options will be ignored."
                print(col.error(msg))
            for action in self._actions:
                if action.required is True:
                    action.required = False
        options = super(Options, self).parse_args(*args)
        return options

def main(args=None):

    if args is None:
        args = sys.argv

    # whatever needs to be called by all pipeline before the options parsing
    from sequana_pipetools.options import before_pipeline
    before_pipeline(NAME)

    # option parsing including common epilog
    options = Options(NAME, epilog=sequana_epilog).parse_args(args[1:])


    # the real stuff is here
    manager = SequanaManager(options, NAME)

    # create the beginning of the command and the working directory
    manager.setup()
    from sequana import logger
    logger.setLevel(options.level)

    # ============================================== sanity checks
    if not os.path.exists(options.samplesheet):
        logger.error(f"{options.samplesheet} file does not exists")
        sys.exit(1)

    if not os.path.exists(options.bcl_directory):
        logger.error(f"{options.bcl_directory} file does not exists")
        sys.exit(1)

    # Check the sample sheet
    from sequana import iem
    try:
        samplesheet = iem.IEM(options.samplesheet)
        samplesheet.validate()
    except Exception as err:
        logger.critical(err)
        logger.critical("""Your sample sheet seems to be incorrect. Before running the pipeline
you will have to fix it. You may use 'sequana samplesheet --quick-fix'""")

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

    if runparam:
        with open(runparam, "r") as fin:
            data = fin.read()
            if "NextSeq" in data and options.merging_strategy != "merge":
                if options.merging_strategy == "none_and_force":
                    msg = "This is a NextSeq. You set the --merging-strategy to"
                    msg += " none_and_force. So, we proceed with no merging strategy"
                    logger.warning(msg)
                if options.merging_strategy == "none":
                    msg = "This is a NextSeq run. You must set the "
                    msg += " --merging-strategy to 'merge'."
                    logger.warning(msg)
                    sys.exit(1)

    if options.from_project is None:
        cfg = manager.config.config
        cfg.general.input_directory = os.path.abspath(options.bcl_directory)
        cfg.bcl2fastq.threads = options.threads
        cfg.bcl2fastq.barcode_mismatch = options.mismatch
        cfg.bcl2fastq.samplesheet_file = os.path.abspath(options.samplesheet)

        from sequana.iem import IEM
        ss = IEM(cfg.bcl2fastq.samplesheet_file)
        ss.validate()


        # this is defined by the working_directory
        #cfg.bcl2fastq.output_directory = "."
        cfg.bcl2fastq.ignore_missing_bcls = not options.no_ignore_missing_bcls
        cfg.bcl2fastq.no_bgzf_compression = not options.bgzf_compression

        if options.merging_strategy == "merge":
            cfg.bcl2fastq.merge_all_lanes = True
        elif options.merging_strategy in  ["none", "none_and_force"]:
            cfg.bcl2fastq.merge_all_lanes = False

        #
        if options.mars_seq:
            cfg.bcl2fastq.options = " --minimum-trimmed-read-length 15 --mask-short-adapter-reads 15 "
            if options.merging_strategy in ["merge"]:
                logger.warning("with --mars-seq option, the merging strategy should be none_and_force")
                cfg.bcl2fastq.merge_all_lanes = False

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown(check_input_files=False)

    if options.run:
        subprocess.Popen(["sh", '{}.sh'.format(NAME)], cwd=options.workdir)

if __name__ == "__main__":
    main()
