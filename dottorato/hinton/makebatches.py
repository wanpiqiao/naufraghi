#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import time
import gzip

from numpy import *
from numpy import matlib
from numpy import random
from scipy.io import loadmat

def mnist(batchsize=100): # for performance reasons the training data
                        # is partitioned in matrixes
    data = loadmat("mnist_all.mat")
    """
    >>> [(m, data[m].shape) for m in data.keys() if "_" not in m]
    [('test1', (1135, 784)),
    ('test0', (980, 784)),
    ('test3', (1010, 784)),
    ('test2', (1032, 784)),
    ('test5', (892, 784)),
    ('test4', (982, 784)),
    ('test7', (1028, 784)),
    ('test6', (958, 784)),
    ('test9', (1009, 784)),
    ('test8', (974, 784)),
    ('train4', (5842, 784)),
    ('train5', (5421, 784)),
    ('train6', (5918, 784)),
    ('train7', (6265, 784)),
    ('train0', (5923, 784)),
    ('train1', (6742, 784)),
    ('train2', (5958, 784)),
    ('train3', (6131, 784)),
    ('train8', (5851, 784)),
    ('train9', (5949, 784))]
    """
    batchdata = concatenate([data[m] for m in data if "train" in m])
    batchdata = array(batchdata, dtype=float32) / 255
    random.seed(0)
    random.shuffle(batchdata)
    batchdata.resize(batchsize, (batchdata.shape[0]/batchsize)+1, batchdata.shape[1])
    """
    >>> batchdata.shape
    (100, 601, 784)
    """
    return batchdata

def usps(batchsize=25): # for performance reasons the training data
                        # is partitioned in matrixes
    filename = "zip.train.gz"
    print "Loading '%s'" % filename
    batchdata = []
    for line in gzip.open(filename).readlines():
        row = line.strip().split(" ")
        number, picture = int(row[0]), map(float, row[1:])
        # normalize inputs
        inputs = picture # in range [-1, 1]
        # digitalize outputs
        #targets = [(i == number) and 1 or -1 for i in range(10)]
        batchdata.append(inputs)
    batchdata = (array(batchdata) + 1) / 2
    random.seed(0)
    random.shuffle(batchdata)
    batchdata.resize(batchsize, (batchdata.shape[0]/batchsize)+1, batchdata.shape[1])
    """
    >>> batchdata.shape
    (100, 601, 784)
    """
    return batchdata
