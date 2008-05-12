#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys
import gzip

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sys.path.append("../")

from bplnn import *

def load_data(filename):
    trace("Loading '%s'" % filename)
    data = []
    for line in gzip.open(filename).readlines():
        row = line.strip().split(" ")
        number, picture = int(row[0]), map(float, row[1:])
        # normalize inputs
        inputs = picture # already [-1, 1]
        # digitalize outputs
        targets = [(i == number) and 1 or -1 for i in range(10)]
        data.append([vector(inputs), vector(targets)])
    print stats(data)
    print "-"*70
    return data

def run():
    trace("USPS dataset", "#")
    patterns = load_data("zip.train.gz")
    n_in = len(patterns[0][0])
    n_out = len(patterns[0][1])
    net = DeepNetwork([n_in, n_in/2, n_in/4, n_out], auto_mode="step")
    print net
    trace("AutoTrain")
    for i in range(1):
        net.prepare(patterns, 1000, 0.05)
    trace("Test1")
    test_patterns = load_data("zip.test.gz")
    net.test(test_patterns)
    trace("FineTrain")
    net.train(patterns, 1000)
    trace("Test2")
    test_patterns = load_data("zip.test.gz")
    net.test(test_patterns)
    print net.dump()



if __name__=="__main__":
    run()
