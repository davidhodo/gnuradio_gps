#!/usr/bin/env python

import numpy

prn_dict = {1: [2, 6],
            2: [3, 7],
            3: [4, 8],
            4: [5, 9],
            5: [1, 9],
            6: [2, 10],
            7: [1, 8],
            8: [2, 9],
            9: [3, 10],
            10: [2, 3],
            11: [3, 4],
            12: [5, 6],
            13: [6, 7],
            14: [7, 8],
            15: [8, 9],
            16: [9, 10],
            17: [1, 4],
            18: [2, 5],
            19: [3, 6],
            20: [4, 7],
            21: [5, 8],
            22: [6, 9],
            23: [1, 3],
            24: [4, 6],
            25: [5, 7],
            26: [6, 8],
            27: [7, 9],
            28: [8, 10],
            29: [1, 6],
            30: [2, 7],
            31: [3, 8],
            32: [4, 9],
            33: [5, 10],
            34: [4, 10],
            35: [1, 7],
            36: [2, 8],
            37: [4, 10]}

class ShiftRegister:
    def __init__(self, order=10, taps=[]):
        self.register = [1] * order
        self.taps = taps

    def sum(self, alternate_taps=None):
        sum_taps = self.taps if alternate_taps is None else alternate_taps
        out = 0
        for tap in sum_taps:
            out += self.register[tap-1]
        return out & 1

    def shift(self):
        new = self.sum()
        out = self.register.pop()
        self.register.insert(0, new)
        return out

    def __str__(self):
        out = ''
        for data in self.register:
            out += str(data)
        return out

def prn_code(prn=1, upsample=None):
    """generate the code sequence for the given prn"""
    g1 = ShiftRegister(taps=[3, 10])
    g2 = ShiftRegister(taps=[2, 3, 6, 8, 9, 10])
    sequence = []
    for count in xrange(1023):
        sequence.append((g1.shift()+g2.sum(prn_dict[prn])) & 1)
        g2.shift()
    if upsample is not None:
        upsequence = []
        for index in range(int(round(len(sequence)*upsample))):
            upsequence.append(sequence[int(index/upsample)])
        sequence = upsequence
    # original
    #gold_code = [1 if entry==0 else -1 for entry in sequence]
    # inverted    
    gold_code = [-1 if entry==0 else 1 for entry in sequence]
    return gold_code


def main():
    # random sequence
    #random_sequence = numpy.random.randint(2, size=1023)
    # gps prn sequence
    random_sequence = prn_code()
    r = []
    for count in xrange(len(gold_code)):
        r.append(numpy.correlate(gold_code, numpy.roll(gold_code, count)))
    print random_sequence[:10]
    import pylab
    pylab.figure()
    pylab.plot(r)
    pylab.show()

if __name__=='__main__':
    main()
