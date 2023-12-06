#
#  This file is part of Sequana software
#
#  Copyright (c) 2016-2021 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os
import sys

import click_completion
import rich_click as click

click_completion.init()

NAME = "demultiplex"

from sequana_pipetools import SequanaManager
from sequana_pipetools.options import *

help = init_click(
    NAME,
    groups={
        "Pipeline Specific": ["--method", "--skip-multiqc"],
    },
)


@click.command(context_settings=help)
@include_options_from(ClickSnakemakeOptions, working_directory="fastq")
@include_options_from(ClickSlurmOptions)
@include_options_from(ClickInputOptions, add_input_readtag=False)
@include_options_from(ClickGeneralOptions)
@click.option(
    "--threads",
    "threads",
    default=4,
    show_default=True,
    type=click.INT,
    help="Number of threads to use during the demultiplexing. ",
)
@click.option("--barcode-mismatch", "mismatch", default=0, type=click.INT, show_default=True)
@click.option(
    "--merging-strategy",
    "merging_strategy",
    required=True,
    type=click.Choice(["merge", "none", "none_and_force"]),
    help="""Merge Lanes or not. options are : merge, none, none_and_force.
            The 'merge' choice merges all lanes. The 'none' choice do NOT merge the lanes.
            For NextSeq runs, we should merge the lanes; if users demultiplex NextSeq
            and set this option to none, an error is raised. If you still want to
            skip the merging step, then set this option to 'none_and_force'. For sc-atac seq, use merge.""",
)
@click.option(
    "--bcl-directory",
    "bcl_directory",
    required=True,
    help="""Directory towards the raw BCL files. This directory should
            contains files such as RunParameters.xml, RunInfo.xml """,
)
@click.option(
    "--sample-sheet",
    "samplesheet",
    required=True,
    default="SampleSheet.csv",
    show_default=True,
    help="Sample sheet filename to be used",
)
@click.option(
    "--no-ignore-missing-bcls",
    "no_ignore_missing_bcls",
    is_flag=True,
    default=False,
    show_default=True,
    help="""In bcl2fastq, the option --ignore-missing-bcls implies that
we assume 'N'/'#' for missing calls. In Sequana_demultiplex, we use that option
by default. If you do not want that behviour, but the one from bcl2fastq, use
this flag(--no-ignore-missing-bcls)""",
)
@click.option(
    "--bgzf-compression",
    "bgzf_compression",
    is_flag=True,
    show_default=False,
    help="""turn on BGZF compression for FASTQ files. By default,
bcl2fastq uses this option; By default we don't. Set --bgzl--compression flag to
set it back""",
)
@click.option(
    "--mars-seq",
    default=False,
    is_flag=True,
    show_default=True,
    help="""Set options to--minimum-trimmed-read-length 15 --mask-short-adapter-reads 15
and do not merge lanes""",
)
@click.option(
    "--scatac-seq",
    default=False,
    is_flag="store_true",
    help="""Set options to perform single cell ATAC demultiplexing using cellranger.""",
)
def main(**options):
    # the real stuff is here
    manager = SequanaManager(options, NAME)
    options = manager.options

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

    cfg = manager.config.config
    cfg.general.input_directory = os.path.abspath(options.bcl_directory)
    cfg.bcl2fastq.threads = options.threads
    cfg.bcl2fastq.barcode_mismatch = options.mismatch
    cfg.general.samplesheet_file = os.path.abspath(options.samplesheet)

    # this is defined by the working_directory
    # cfg.bcl2fastq.output_directory = "."
    cfg.bcl2fastq.ignore_missing_bcls = not options.no_ignore_missing_bcls
    cfg.bcl2fastq.no_bgzf_compression = not options.bgzf_compression

    if options.merging_strategy == "merge":
        cfg.bcl2fastq.merge_all_lanes = True
    elif options.merging_strategy in ["none", "none_and_force"]:
        cfg.bcl2fastq.merge_all_lanes = False

    #
    if options.mars_seq:
        cfg.bcl2fastq.options = " --minimum-trimmed-read-length 15 --mask-short-adapter-reads 15 "
        if options.merging_strategy in ["merge"]:
            logger.warning("with --mars-seq option, the merging strategy should be none_and_force")
            cfg.bcl2fastq.merge_all_lanes = False
        cfg.general.mode = "bcl2fastq"
    elif options.scatac_seq:
        cfg.cellranger_atac.options = ""
        cfg.general.mode = "cellranger_atac"
    else:  # All other cases with bcl2fastq
        from sequana.iem import IEM

        cfg.general.mode = "bcl2fastq"
        try:
            ss = IEM(cfg.general.samplesheet_file)
            ss.validate()
        except Exception as err:
            logger.critical(err)
            logger.critical(
                """Your sample sheet seems to be incorrect. Before running the pipeline you will have to fix it. You may use 'sequana samplesheet --quick-fix'"""
            )

    # finalise the command and save it; copy the snakemake. update the config
    # file and save it.
    manager.teardown(check_input_files=False)


if __name__ == "__main__":
    main()
