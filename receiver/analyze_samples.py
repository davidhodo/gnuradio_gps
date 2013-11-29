#!/usr/bin/env python

# TOFIX: acquisition at a later index does not include the index delay;
#       only the code phase from the start of the file


import os
import sys
import numpy
import matplotlib.pyplot as plt
import numpy
import math
import logging
from optparse import OptionParser
import UsrpData

logger = logging.getLogger('soft')

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = OptionParser(usage="%prog: [options] filename")
    parser.add_option("-d", "--delay", type="float", default=1.0,
                      metavar="seconds", help="Time to delay into file before processing [default=%default]")
    parser.add_option("-r", "--rate", type="float", default=25.0e6,
                      metavar="Hz", help="Sample frequency (f_s) [default=%default]")
    parser.add_option("-i", "--f_if", type="float", default=0.0,
                      metavar="Hz", help="Intermediate frequency (f_if) [default=%default]")
    parser.add_option("-f", "--format", type="string", default="sc16",
                      help="File format {sc16, fc32, ??} [default=%default]")
    parser.add_option("-t", "--time", type="float", default=0.001,
                      help="Length of data to analyze [default=%default]")
    parser.add_option("-p", "--plot", action="store_true", dest="plot",
                      help="Plot data samples. [default=%default]")
    parser.add_option("-h", "--hist", action="store_true", dest="histogram",
                      help="Plot histogram of data samples. [default=%default]")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    filename = args[0]
    if not os.path.isfile(filename):
        print("File does not exist: " + filename)
        sys.exit(1)

    print("Opening file for analysis:")
    print(filename)
    data_store = UsrpData.USRPData(filename, f_s=options.rate, f_if=options.f_if, file_format=options.format)
    if options.delay > 0:
        data_store.delay(delay_time=options.delay)

    data_chunk = data_store.read_array(time_interval=options.time)

    print("Standard deviation:")
    std_dev = numpy.std(data_chunk)
    print(std_dev)

    if options.histogram:
        print("Plotting hisogram.")
        plt.hist(data_chunk, bins=100)
    #print(std_dev_imag)
    # plt.hist(real_vector[1:200000], bins=100)
    # plt.show()