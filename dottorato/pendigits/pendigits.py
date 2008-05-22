#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))

sys.path.append("../")

from bplnn import *

def load_patterns(filename):
    trace("Loading '%s'" % filename)
    inputs = []
    targets = []
    for line in open(filename).readlines():
        row = map(int, line.split(","))
        stroke, number = row[:-1], row[-1]
        # normalize inputs
        inputs.append([float(i)/100 for i in stroke])
        # digitalize outputs
        targets.append([int(i == number) for i in range(10)])
    print stats(inputs, targets)
    print "-"*70
    return np.mat(inputs), np.mat(targets)

def run():
    trace("PenDigits dataset", "#")
    inputs, targets = load_patterns("pendigits.tra")
    test_inputs, test_targets = load_patterns("pendigits.tes")
    n_in = inputs.shape[1] # 16
    n_out = targets.shape[1] # 10
    net = DeepNetwork([n_in, 20, 15, n_out])
    print net
    net.prepare(inputs, targets, 200, 0.05)
    net.test(test_inputs, test_targets)
    info(" auto test ".center(70, "-"))
    net.train(inputs, targets, 200)
    net.test(test_inputs, test_targets)



if __name__=="__main__":
    run()
