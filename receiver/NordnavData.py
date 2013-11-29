#!/usr/bin/env python


class NordnavData(object):
    def __init__(self, file_name, f_s=16.3676e6, f_if=4.1304e6,
            packed=True, preloadSec=1., complex=False):
        self.data_source = open(file_name, 'rb')
        self.f_s = f_s
        self.f_if = f_if
        self.f_L1 = 154 * 10.23e6
        self.packed = packed
        self.loaded = []
        self.loadedIndex = -1
        self.preload = int(preloadSec * self.f_s)
        self.complex = complex
        self.printAcqData = 1
        self.printCorData = 1

    def read(self, time_interval=0.001, pull=False):
        """Get the time_interval's worth of data"""
        data = []
        bytes = int(round(time_interval * self.f_s))
        if self.packed:
            bytes = bytes / 4
        file_point = self.data_source.tell()
        data = [self.next_byte() for sample in xrange(bytes)]
        if pull:
            self.data_source.seek(file_point)
        return data

    def delay(self, delayTime=0.):
        """Delay into the data file"""
        bytes = int(round(delayTime * self.f_s))
        self.data_source.seek(bytes)

    def tell(self):
        """Return the current file point"""
        return self.data_source.tell()

    def read_array(self, time_interval=0.001, pull=False, fromIndex=None):
        """Return the data as an array"""

        bytes = int(round(time_interval * self.f_s))
        file_point = self.data_source.tell()
        if fromIndex is None:
            if self.packed or self.complex:
                output = self.read(time_interval, pull=pull)
                if pull:
                    self.data_source.seek(file_point)
                if len(output) < bytes:
                    return None
                else:
                    return array(output)
            else:
                output = numpy.fromfile(self.data_source, 'b', bytes)
                if pull:
                    self.data_source.seek(file_point)
                if len(output) < bytes:
                    return None
                return output
        else:

            self.data_source.seek(int(round(fromIndex)))
            if self.packed or self.complex:
                output = self.read(time_interval, pull=pull)
                if pull:
                    self.data_source.seek(file_point)
                if len(output) < bytes:
                    return None
                else:
                    return array(output)
            else:
                output = numpy.fromfile(self.data_source, 'b', bytes)
                if pull:
                    self.data_source.seek(file_point)
                if len(output) < bytes:
                    return None
                return output

    def next_byte(self):
        if self.packed:
            return self.unpack_packed(self.data_source.read(1))
        elif self.complex:
            return self.unpack_IQ(self.data_source.read(1))
        else:
            return self.unpack(self.data_source.read(1))

    def unpack(self, byte):
        if len(byte) == 0:
            return []
        return [struct.unpack('b', byte)[0]]

    def unpack_packed(self, byte):
        if len(byte) == 0:
            return []
        b = struct.unpack('b', byte)[0]
        b1 = sign_mag[b & 3]
        b2 = sign_mag[(b >> 2) & 3]
        b3 = sign_mag[(b >> 4) & 3]
        b4 = sign_mag[(b >> 6) & 3]
        return [b4, b3, b2, b1]

    def unpack_IQ(self, byte):
        if len(byte) == 0:
            return []
        b = struct.unpack('B', byte)[0]
        I = fourBit[b>>4]
        Q = fourBit[b&15]
        return complex(Q, I)