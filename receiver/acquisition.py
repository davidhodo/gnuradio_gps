#!/usr/bin/env python

# TOFIX: acquisition at a later index does not include the index delay;
#       only the code phase from the start of the file


import os
import sys
import numpy
from numpy import cos, sin
from numpy import array, zeros, eye
import prn_generator
import logging
from optparse import OptionParser
import UsrpData

logger = logging.getLogger('soft')


class Acquisition(object):
    def acquire(self, data, plot=False, threshold=2.5):
        visible = []
        for prn in range(1, 33):
            logger.info('Acquisition.acquire():searching for prn ' + str(prn))
            acq1 = self.acquire_parallel(data, prn)
            acq2 = self.acquire_parallel(data, prn, delay=0.001)
            acq = acq1 if acq1[0] > acq2[0] else acq2
            if acq[0] > threshold:
                acq = self.acquire_parallel(data, prn, plot, freq_estimate=acq[1])
                logger.info('Acquisition.acquire():\tfound at doppler ' + str(acq[1]) + ' and code phase ' + str(acq[2]) + ' with mag ' + str(acq[0]))
                logger.info('Acquisition.acquire():acquired:' + str((prn, acq[1], acq[2])))
                visible.append((prn, acq[1], acq[2]+data.tell()))
            else:
                logger.info('Acquisition.acquire():\tnot visible with mag ' + str(acq[0]))
        return visible

    def acquire_parallel(self, data, prn, plot=False, freq_estimate=None, delay=None):
        if delay is None:
            data_1ms = data.read_array(pull = True)
        else:
            samples_count = len(data.read_array(pull=True))
            data_1ms = data.read_array(delay+0.001, pull=True)[-samples_count:]
        signal_range = numpy.arange(float(len(data_1ms)))
        if freq_estimate is None:
            doppler_bins = numpy.arange(-10000., 10000., 500.)
        else:
            doppler_bins = numpy.arange(freq_estimate-500., freq_estimate+500., 10.)
        code = array(prn_generator.prn_code(prn, data.f_s*1e-3/1023))
        local_code = numpy.fft.fft(code).conj()
        best = None
        best_list = None
        if plot:
            x, y, z = [], [], []
        for dindex in range(len(doppler_bins)):
            dopp = doppler_bins[dindex]
            if data.complex:
                IQ = data_1ms * numpy.exp(2j*numpy.pi*(data.f_if + dopp) \
                        * signal_range / data.f_s)
            else:
                inphase = cos(2.*numpy.pi*(data.f_if + dopp) / data.f_s *
                                    signal_range) * data_1ms
                quadphase = sin(2.*numpy.pi*(data.f_if + dopp) / data.f_s *
                                    signal_range) * data_1ms
                # TODO: append directly to array
                IQ = []
                for i, q in zip(inphase, quadphase):
                    IQ.append(complex(i, q))
            signal = numpy.fft.fft(array(IQ))
            res = numpy.fft.ifft(signal * local_code)
            res_mag = numpy.abs(res) ** 2
            res_max_index = res_mag.argmax()
            if plot:
                x.extend([dopp]*len(res_mag))
                y.extend(range(len(res_mag)))
                z.extend(list(res_mag))
            if best is None or best[0] < res_mag[res_max_index]:
                best = (res_mag[res_max_index], dopp, res_max_index)
                best_list = res_mag
        chip_width = numpy.ceil(data.f_s * 1e-3 * 0.5 / 1023)
        if chip_width < best[2] < len(best_list) - chip_width:
            search_list = numpy.concatenate((best_list[:best[2]-chip_width], best_list[best[2]+chip_width+1:]))
        else:
            search_list = best_list[int((best[2]+chip_width+1) % len(best_list)):int((best[2]-chip_width) % len(best_list))]
        next_best = max(search_list)
        if plot:
            import pylab
            from mpl_toolkits.mplot3d import Axes3D
            pylab.figure()
            pylab.plot(code)
            fig = pylab.figure()
            ax = Axes3D(fig)
            ax.scatter(x, y, z)
            ax.set_xlabel('Doppler (Hz)')
            ax.set_ylabel('Code Phase (samples)')
            ax.set_zlabel('Magnitude')
            pylab.show()
        return best[0]/next_best, best[1], best[2]
        
    def acquire_serial(self, data, prn, plot=False):
        data_1ms = data.read_array()
        signal_range = numpy.arange(float(len(data_1ms)))
        doppler_bins = numpy.arange(-5000., 5000., 500.)
        code = array(sigsim.prn_code(prn, 16))
        res = zeros((len(doppler_bins), len(code)))
        local_code = code[:]
        best = None
        if plot:
            x, y, z = [], [], []
        for dindex in range(len(doppler_bins)):
            dopp = doppler_bins[dindex]
            inphase = cos(2.*numpy.pi*(data.f_if + dopp) / data.f_s *
                                signal_range)
            quadphase = sin(2.*numpy.pi*(data.f_if + dopp) / data.f_s *
                                signal_range)
            for shift in range(len(code)):
                local_code = circ_shift(code, shift)
                signal = data_1ms * local_code
                I = signal * inphase
                Q = signal * quadphase
                res_squared_mag = I.sum()**2 + Q.sum()**2
                if best is None or best[0] < res_squared_mag:
                    best = (res_squared_mag, dopp, shift)
                if plot:
                    x.append(dopp)
                    y.append(shift)
                    z.append(res_squared_mag)
        if plot:
            import pylab
            from mpl_toolkits.mplot3d import Axes3D
            pylab.figure()
            pylab.plot(code)
            fig = pylab.figure()
            ax = Axes3D(fig)
            ax.scatter(x, y, z)
        return best

if __name__ == '__main__':

    #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = OptionParser(usage="%prog: [options] filename")
    parser.add_option("-d", "--delay", type="float", default=5.0,
        metavar="seconds", help="Time to delay into file before processing [default=%default]")
    parser.add_option("-r", "--rate", type="float", default=25.0e6,
        metavar="Hz", help="Sample frequency (f_s) [default=%default]")
    parser.add_option("-i", "--f_if", type="float", default=0.0,
        metavar="Hz", help="Intermediate frequency (f_if) [default=%default]")
    parser.add_option("-f", "--format", type="string", default="sc16",
        help="File format {sc16, fc32, ??} [default=%default]")
    parser.add_option("-t", "--threshold", type="float", default=2.5,
        help="Acquisition threshold [default=%default]")
    parser.add_option("-p", "--plot", action="store_true", dest="plot",
        help="Results are plotted if set.")

    (options, args) = parser.parse_args()


    if len(args) !=1:
        parser.print_help()
        sys.exit(1)

    filename = args[0]
    if not os.path.isfile(filename):
        print("File does not exist: " + filename)
        sys.exit(1)

    print("Opening file for acquisition:")
    print(filename)
    data_store = UsrpData.USRPData(filename, f_s=options.rate, f_if=options.f_if, file_format=options.format)

    if (options.delay>0):
        data_store.delay(options.delay)

    acq_object = Acquisition()
    visible_svs = acq_object.acquire(data_store, plot=options.plot, threshold=options.threshold)
    print(str(len(visible_svs))+ " Visible Svs:")
    print(visible_svs)