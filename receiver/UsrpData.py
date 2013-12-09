#!/usr/bin/env python

import struct
from numpy import array, zeros, eye
from optparse import OptionParser
import sys
import os

class USRPData(object):
    def __init__(self, file_name, f_s=25.0e6, f_if=0.0,
            file_format="sc16"):
        self.data_source = open(file_name, 'rb')
        self.f_s = f_s
        self.f_if = f_if
        self.f_l1 = 154 * 10.23e6
        self.file_format = file_format
        self.loaded = []
        self.loaded_index = -1
        self.complex = True
        if self.file_format == "fc32":
            self.bytes_per_sample = 8
        else:
            self.bytes_per_sample = 4

    def read(self, time_interval=0.001, pull=False):
        """Get the time_interval's worth of data"""
        # determine num of samples based on interval, sample rate, and bytes per sample
        samples = int(round(time_interval * self.f_s))

        # get the current location in the file (for pull)
        file_point = self.data_source.tell()
        # read the selected num of samples starting at the current location
        data_samples = [self.next_sample() for ii in xrange(samples)]

        # reset the file pointer to its original location if requested
        if pull:
            self.data_source.seek(file_point)

        # make sure we got the num of bytes requested
        if len(data_samples) < samples:
            return []
        else:
            return data_samples

    def delay(self, delay_time=0.001):
        """Delay into the data file"""
        bytes_to_delay = int(round(delay_time * self.f_s)) * self.bytes_per_sample
        self.data_source.seek(bytes_to_delay)

    def tell(self):
        """Return the current file point"""
        return self.data_source.tell()

    def read_array(self, time_interval=0.001, pull=False, from_index=None):
        """Return the data as an array"""

        file_point = self.data_source.tell()

        if from_index is not None:
            self.data_source.seek(int(round(from_index)))

        output_data = array(self.read(time_interval, pull=pull))

        if pull:
            self.data_source.seek(file_point)

        return output_data

    def next_sample(self):
        return self.unpack(self.data_source.read(self.bytes_per_sample))

    def unpack(self, sample_bytes):
        if len(sample_bytes) == 0:
            return None

        if self.file_format == "fc32":
            unpacked = struct.unpack('ff', sample_bytes)
            # TODO: check the order of this, 0 then 1??
            return complex(unpacked[0], unpacked[1])
        elif self.file_format == "sc16":
            unpacked = struct.unpack('hh', sample_bytes)
            return complex(unpacked[0], unpacked[1])
        else:
            print("Unsupported file format: " + self.file_format)
            return None

if __name__ == '__main__':

    parser = OptionParser(usage="%prog: [options] filename")
    parser.add_option("-r", "--rate", type="float", default=25.0e6,
                      metavar="Hz", help="Sample frequency (f_s) [default=%default]")
    parser.add_option("-i", "--f_if", type="float", default=0.0,
                      metavar="Hz", help="Intermediate frequency (f_if) [default=%default]")
    parser.add_option("-f", "--format", type="string", default="sc16",
                      help="File format {sc16, fc32, ??} [default=%default]")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    filename = args[0]
    if not os.path.isfile(filename):
        print("File does not exist: " + filename)
        sys.exit(1)

    print("Opening file:")
    print(filename)
    data_store = USRPData(filename, f_s=options.rate, f_if=options.f_if, file_format=options.format)

    result = data_store.read()
    print("Size: " + str(len(result)))
    print("First 20 samples:")
    print(result[1:20])
