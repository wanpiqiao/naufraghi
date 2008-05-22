#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys
import gzip

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sys.path.append("../")

from bplnn import *

def load_patterns(filename):
    trace("Loading '%s'" % filename)
    inputs = []
    targets = []
    for line in gzip.open(filename).readlines():
        row = line.strip().split(" ")
        number, picture = int(row[0]), map(float, row[1:])
        # normalize inputs
        inputs.append(picture) # already [-1, 1]
        # digitalize outputs
        targets.append([(i == number) and 1 or -1 for i in range(10)])
    print stats(inputs, targets)
    print "-"*70
    return np.mat(inputs), np.mat(targets)

def run():
    trace("USPS dataset", "#")
    inputs, targets = load_patterns("zip.train.gz")
    test_inputs, test_targets = load_patterns("zip.test.gz")
    n_in = inputs.shape[1]
    n_out = targets.shape[1]
    net = DeepNetwork([n_in, 500, 250, 100, n_out])
    print net
    trace("AutoTrain")
    net.prepare(inputs, 100, 0.05)
    net.test(test_inputs, test_targets)
    trace("FineTrain")
    net.train(inputs, targets, 100)
    net.test(test_inputs, test_targets)


if __name__=="__main__":
    run()
