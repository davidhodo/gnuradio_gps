#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov 25 14:23:16 2013
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time
import sys

import numpy
import math

def to_imag(x):
    out = x&0xffff
    if ((out&0x8000)>0):
        out = out - math.pow(2,16)
    return out

def to_real(x):
    return (x>>16)

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option, usage="%prog: [options] directory")
        parser.add_option("-r", "--rate", type="eng_float", default=25e6,
            metavar="samples/second", help="Sample rate [default=%default]")
        parser.add_option("-b", "--bw", type="eng_float", default=0,
            metavar="Hz", help="Bandwidth [default=%default]")
        parser.add_option("-o", "--offset", type="eng_float", default=0,
            metavar="Hz", help="Local oscillator offset - Hz [default=%default]")
        parser.add_option("-g", "--gain", type="eng_float", default=28                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ,
            metavar="dB", help="RX front-end gain [default=%default]")
        parser.add_option("-t", "--time", type="eng_float", default=180,
            metavar="sec", help="Length of time to record [default=%default]")
        parser.add_option("-f", "--format", type="string", default="sc16",
            help="File format: {sc16, fc32, ??} [default=%default]")
        parser.add_option("-w", "--wire_format", type="string", default="sc16",
            help="Wire format: {sc8, sc16} [default=%default]")        
        parser.add_option("", "--freq", type="eng_float", default=1.57542e9,
            metavar="Hz", help="Center frequency [default=%default]")
        parser.add_option("-a", "--stream_args", type="string", default="s",
            help="Stream arguments [default=%default]") 

        (options, args) = parser.parse_args()

        # if len(args) != 1:
        #     parser.print_help()
        #     sys.exit(1)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate =  options.rate
        self.lo_off =  options.offset
        self.freq_l1 =  options.freq
        self.gain = options.gain
        self.record_time = options.time
        self.file_format = options.format
        self.wire_format = options.wire_format
        self.bandwidth = options.bw
        self.stream_args = options.stream_args


        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format=self.file_format,
                otw_format=self.wire_format,
                channels=range(1),
                args=self.stream_args,
            ),
        )
        self.uhd_usrp_source_0.set_clock_source("gpsdo", 0)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_l1, self.lo_off), 0)
        self.uhd_usrp_source_0.set_gain(self.gain, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 0)
        
        self.blocks_vector_sink_x_0 = blocks.vector_sink_i(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_vector_sink_x_0, 0))

if __name__ == '__main__':
    tb = top_block()
    tb.start()
    #print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_locked"))
    #print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_time"))
    #print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_gpgga"))
    #print(tb.uhd_usrp_source_0.get_mboard_sensor("ref_locked"))
    print("Warming up...")
    time.sleep(5.0)
    print("Reset vector and record...")
    tb.blocks_vector_sink_x_0.reset()
    time.sleep(2.0)
    tb.stop()
    print("Done sampling. Analyzing results.")

    print("Converting to real only.")
    sample_vector=tb.blocks_vector_sink_x_0.data()
    real_vector=[to_real(x) for x in sample_vector]
    print("Samples 1 to 10:")
    print(real_vector[1:10])
    print("Captured sample length:")
    print(len(real_vector))
    std_dev_real = numpy.std(real_vector)
    print("Standard deviation: " + str(std_dev_real))
    max_value = numpy.amax(real_vector)
    print("Maximum value: " + str(max_value))
    peak_setting = max_value/32768.0
    print("Suggested peak setting: " + str(peak_setting))