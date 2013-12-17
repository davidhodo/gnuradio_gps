#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Dec 16 18:24:05 2013
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time
import wx

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20e6
        self.lo_off = lo_off = 0
        self.gain = gain = 10
        self.freq_l2 = freq_l2 = 1.22760e9
        self.freq_l1 = freq_l1 = 1.57542e9

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	device_addr="addr0=192.168.10.3,addr1=192.168.10.2",
        	stream_args=uhd.stream_args(
        		cpu_format="sc16",
        		otw_format="sc8",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_sink_0.set_clock_source("gpsdo", 0)
        self.uhd_usrp_sink_0.set_time_source("gpsdo", 0)
        self.uhd_usrp_sink_0.set_clock_source("mimo", 1)
        self.uhd_usrp_sink_0.set_time_source("mimo", 1)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(freq_l1, lo_off), 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(freq_l2, lo_off), 1)
        self.uhd_usrp_sink_0.set_gain(gain, 1)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 1)
        self.blocks_file_source_0 = blocks.file_sink(gr.sizeof_int*1, "/home/is4s/devel/gnuradio_gps/usrp_l2.dat", False)
        self.blocks_file_source_0.set_unbuffered(False)
        self.blocks_file_source_1 = blocks.file_sink(gr.sizeof_int*1, "/home/is4s/devel/gnuradio_gps/usrp_l1.dat", False)
        self.blocks_file_source_1.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_sink_0, 0), (self.blocks_file_source_0, 0))
        self.connect((self.uhd_usrp_sink_0, 1), (self.blocks_file_source_1, 0))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.start()
    tb.wait()
    tb.stop()

