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

import matplotlib.pyplot as plt
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

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 25e6
        self.lo_off = lo_off = 0
        self.freq_l1 = freq_l1 = 1.57542e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format="sc16",
                otw_format="sc16",
                channels=range(1),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source("gpsdo", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(freq_l1, lo_off), 0)
        self.uhd_usrp_source_0.set_gain(35, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        #self.uhd_usrp_source_0.set_antenna("TX/RX", 0)

        #self.uhd_usrp_source_0.set_bandwidth(20e6, 0)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_i(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_vector_sink_x_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_lo_off(self):
        return self.lo_off

    def set_lo_off(self, lo_off):
        self.lo_off = lo_off
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_l1, self.lo_off), 0)

    def get_freq_l1(self):
        return self.freq_l1

    def set_freq_l1(self, freq_l1):
        self.freq_l1 = freq_l1
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_l1, self.lo_off), 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    time.sleep(0.5)
    tb.blocks_vector_sink_x_0.reset()
    time.sleep(0.5)
    tb.stop()
    sample_vector=tb.blocks_vector_sink_x_0.data()
    print("Converting to real only.")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    real_vector=[to_real(x) for x in sample_vector]
    imag_vector=[to_imag(x) for x in sample_vector]
    print("Samples:")
    print(sample_vector[1:20])
    print("Real samples:")
    print(real_vector[1:20])
    print("Imag samples:")
    print(imag_vector[1:20])
    print("Type:")
    print(type(real_vector[1]))
    print("Captured sample length:")
    print(len(real_vector))
    std_dev_real = numpy.std(real_vector)
    #std_dev_imag = numpy.std(imag_vector)
    print("Standard deviation:")
    print(std_dev_real)
    #print(std_dev_imag)
    # plt.hist(real_vector[1:200000], bins=100)
    # plt.show()