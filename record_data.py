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


class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option, usage="%prog: [options] directory")
        parser.add_option("-r", "--rate", type="eng_float", default=25e6,
            metavar="samples/second", help="Sample rate [default=%default]")
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
        parser.add_option("", "--freq", type="eng_float", default=1.57542e6,
            metavar="Hz", help="Center frequency [default=%default]")

        (options, args) = parser.parse_args()

        if len(args) != 1:
            parser.print_help()
            sys.exit(1)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = options.rate
        self.lo_off = lo_off = options.offset
        self.freq_l1 = freq_l1 = options.freq
        self.gain = gain = options.gain
        self.record_time = record_time = options.time
        self.file_format = file_format = options.format
        self.wire_format = wire_format = options.wire_format
        self.directory = directory = args[0]

        self.filename = directory + "usrp_data_" + str(samp_rate/1e6) + "Msps_" + file_format + "_" + str(gain) + "dB_" +  time.strftime("%Y_%m_%d-%H_%M_%S") + ".bin"

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format=file_format,
                otw_format=wire_format,
                channels=range(1),
            ),
        )
        self.uhd_usrp_source_0.set_clock_source("gpsdo", 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(freq_l1, lo_off), 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        #self.uhd_usrp_source_0.set_bandwidth(20e6, 0)
        import pdb; pdb.set_trace()
        if self.file_format == "fc32":
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*2, self.filename, False)
        else:
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_int*1, self.filename, False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0, 0))

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
    tb = top_block()
    tb.start()
    print("Recording for " + str(tb.record_time) + " seconds to file:")
    print(tb.filename)
    time.sleep(tb.record_time)
    tb.stop()
    print("Recording finished.")
   