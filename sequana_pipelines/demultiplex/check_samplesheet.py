# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
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
import sys, time, optparse
from re import findall


def check_samplesheet(filename):
    """This function checks whether the sample sheet is correctly formatted

    Checks for:
    * presence of ; at the end of lines indicated an edition with excel that
      wrongly transformed the data into a pure CSV file
    * inconsistent numbers of columns in the [DATA] section, which must be
      CSV-like section

    """

    # could use logger, but simpler for now
    prefix = "ERROR  [sequana_pipelines.demultiplex.check_samplesheet]: "
    try:
        with open(filename, "r") as fp:
           line = fp.readline()
           cnt = 1
           if line.rstrip().endswith(";") or line.rstrip().endswith(","):
               sys.exit(prefix + "Unexpected ; or , found at the end of line {} (and possibly others). Please use IEM to format your SampleSheet. Try sequana_fix_samplesheet for extra ; or , ".format(cnt))

           while line:
               line = fp.readline()
               cnt += 1
               if "[Data]" in line:
                   line = fp.readline()
                   cnt += 1
                   if len(line.split(',')) < 2 or "Sample" not in line:
                       sys.exit(prefix + ": No header found after [DATA] section")
                   line = fp.readline()
                   cnt += 1
                   nb_col = len(line.split(','))
                   while line:
                       if len(line.split(',')) != nb_col:
                           sys.exit(prefix + "Different number of column in [DATA] section on line: "+str(cnt))
                       line = fp.readline()
                       cnt += 1
    except Exception as e:
       raise ValueError("type error: " + str(e))

    return 0

def main():
    if len(sys.argv) == 1:
        sys.argv += ["--help"]

    #Parse command line options
    parser = optparse.OptionParser()

    parser.add_option("-s", "--samplesheet", dest="file", type= "string",
                help="SampleSheet path [required]", metavar="FILE")

    (options, args) = parser.parse_args()
    check_samplesheet(options.file)



if __name__=="__main__":
    main()



