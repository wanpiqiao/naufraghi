#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sys.path.append("../")

from bplnn import *

def load_data(filename):
    trace("Loading '%s'" % filename)
    data = []
    for line in open(filename).readlines():
        row = map(int, line.split(","))
        stroke, number = row[:-1], row[-1]
        # normalize inputs
        inputs = [float(i)/100 for i in stroke]
        # digitalize outputs
        targets = [int(i == number) for i in range(10)]
        data.append([vector(inputs), vector(targets)])
    print stats(data)
    print "-"*70
    return data

def run():
    trace("PenDigits dataset", "#")
    patterns = load_data("pendigits.tra")
    test_patterns = load_data("pendigits.tes")
    n_in = len(patterns[0][0]) # 16
    n_out = len(patterns[0][1]) # 10
    net = DeepNetwork([n_in, 14, 12, n_out], auto_mode="step")
    print net
    for i in range(1): # multiple rounds are not so good...
        print "prepare round", i
        net.prepare(patterns, 100, 0.05)
        net.test(test_patterns)
    #print net.dump()
    print "!"*20, "auto test", "!"*20
    net.train(patterns, 10000)
    net.test(test_patterns)



if __name__=="__main__":
    run()
