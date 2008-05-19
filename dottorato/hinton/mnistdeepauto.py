#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import time

import numpy as N
from numpy import matlib

import makebatches
import rbm

# Version 1.000
#
# Code provided by Ruslan Salakhutdinov and Geoff Hinton
#
# Permission is granted for anyone to copy, use, modify, or distribute this
# program and accompanying programs and documents for any purpose, provided
# this copyright notice is retained and prominently displayed, along with
# a note saying that the original programs are available from our
# web page.
# The programs and documents are distributed without any warranty, express or
# implied.  As the programs were written for research purposes only, they have
# not been tested to the degree that would be advisable in any important
# application.  All use of these programs is entirely at the user's own risk.

start_time = time.time()
# This program pretrains a deep autoencoder for MNIST dataset
# You can set the maximum number of epochs for pretraining each layer
# and you can set the architecture of the multilayer net.

maxepoch = 10 #In the Science paper we use maxepoch=50, but it works just fine.
numhid = 1000/2
numpen = 500/2
numpen2 = 250/2
numopen = 30/2

#print 'Converting Raw files into Matlab format'
#converter.run()
# Downloaded mist_all.mat from http://www.cs.toronto.edu/~roweis/data.html

print 'Pretraining a deep autoencoder.'
print 'The Science paper used 50 epochs. This uses %3d' % maxepoch

batchdata = makebatches.usps()
numbatches, numcases, numdims = N.shape(batchdata)

print 'Pretraining Layer 1 with RBM: %d-%d' % (numdims, numhid)
layer = rbm.run(maxepoch, numhid, batchdata)
hidrecbiases = layer["bias_hid"]
#save(mnistvh, vishid, hidrecbiases, visbiases)

print 'Pretraining Layer 2 with RBM: %d-%d' % (numhid, numpen)
batchdata = layer["outprobs"]
numhid = numpen
layer = rbm.run(maxepoch, numhid, batchdata)
hidpen = layer["weights"]
penrecbiases = layer["bias_hid"]
hidgenbiases = layer["bias_vis"]
#save(mnisthp, hidpen, penrecbiases, hidgenbiases)

print 'Pretraining Layer 3 with RBM: %d-%d' % (numpen, numpen2)
batchdata = layer["outprobs"]
numhid = numpen2
layer = rbm.run(maxepoch, numhid, batchdata)
hidpen2 = layer["weights"]
penrecbiases2 = layer["bias_hid"]
hidgenbiases2 = layer["bias_vis"]
#save(mnisthp2, hidpen2, penrecbiases2, hidgenbiases2)

print 'Pretraining Layer 4 with RBM: %d-%d' % (numpen2, numopen)
batchdata = layer["outprobs"]
numhid = numopen
layer = rbm.run(maxepoch, numhid, batchdata, 'linear')
hidtop = layer["weights"]
toprecbiases = layer["bias_hid"]
topgenbiases = layer["bias_vis"]
#save(mnistpo, hidtop, toprecbiases, topgenbiases)

print "Pretraining done in", time.time() - start_time, "seconds"

#backprop.run()

