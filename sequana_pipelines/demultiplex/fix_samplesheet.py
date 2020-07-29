# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#      Dimitri Desvillechabrol <dimitri.desvillechabrol@pasteur.fr>, 
#          <d.desvillechabrol@gmail.com>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import sys, time, optparse, argparse
from re import findall


def main():
    if len(sys.argv) == 1:
        sys.argv += ['--help']
    #Parse command line options
    parser = optparse.OptionParser()

    parser.add_option("-s", "--samplesheet", dest="infile", type= "string",
                help="SampleSheet path [required]", metavar="FILE")
    parser.add_option("-o", "--outfile", dest="outfile", default="SampleSheetFixed.csv", 
                type= "string",
                help="New SampleSheet file", metavar="FILE")
    parser.add_option("--fix-semicolons", dest="fix1", action="store_true")

    (options, args) = parser.parse_args()

    if options.outfile == options.infile:
        raise ValueError("output filename cannot be the input filename")

    # if we find the data section, and we get after the header:
    # So, if we have ; we remove them but , cannot be removed safely.
    # they may be part of the data. In theory this should be formatted correctly
    # since excel we add comma in other section but not in data, which is
    # already a CSV-like structure
    found_data = False
    if options.fix1:
        print("Fixing semicolons if any found")
        with open(options.infile) as fin:
            with open(options.outfile, "w") as fout:
                for line in fin.readlines():

                    if line.startswith('[Data]'):
                        found_data = True

                    if found_data:
                        line = line.replace(";", ",")
                    else:
                        line = line.strip().rstrip(";")
                        line = line.replace(";", ",")
                        line = line.strip().rstrip(",")
                    fout.write(line.strip("\n")+"\n")

    if not options.fix1:
        print("Nothing done. Please use --fix-semicolons")
        sys.exit(0)

    print("Please check the content of {}".format(options.outfile))

if __name__=="__main__":
    main()



