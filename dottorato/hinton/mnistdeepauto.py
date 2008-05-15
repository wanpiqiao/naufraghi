#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import time

from numpy import *
import numpy.matlib as m

import rbm
import rbmhidlinear

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


# This program pretrains a deep autoencoder for MNIST dataset
# You can set the maximum number of epochs for pretraining each layer
# and you can set the architecture of the multilayer net.

maxepoch = 10 #In the Science paper we use maxepoch=50, but it works just fine. 
numhid = 1000
numpen = 500
numpen2 = 250
numopen = 30

print 'Converting Raw files into Matlab format'
converter.run()

print 'Pretraining a deep autoencoder.'
print 'The Science paper used 50 epochs. This uses %3d' % maxepoch

makebatches.run()
numcases, numdims, numbatches = shape(batchdata)

print 'Pretraining Layer 1 with RBM: %d-%d' % (numdims, numhid)
restart = 1
rbm.run()
hidrecbiases = hidbiases
save(mnistvh, vishid, hidrecbiases, visbiases)

print 'Pretraining Layer 2 with RBM: %d-%d' % (numhid, numpen)
batchdata = batchposhidprobs
numhid = numpen
restart = 1
rbm.run()
hidpen = vishid
penrecbiases = hidbiases
hidgenbiases = visbiases
save(mnisthp, hidpen, penrecbiases, hidgenbiases)

print 'Pretraining Layer 3 with RBM: %d-%d' % (numpen, numpen2)
batchdata = batchposhidprobs
numhid = numpen2
restart = 1
rbm.run()
hidpen2 = vishid
penrecbiases2 = hidbiases
hidgenbiases2 = visbiases
save (mnisthp2, hidpen2, penrecbiases2, hidgenbiases2)

print 'Pretraining Layer 4 with RBM: %d-%d' % (numpen2, numopen)
batchdata = batchposhidprobs
numhid = numopen
restart = 1
rbmhidlinear.run()
hidtop = vishid
toprecbiases = hidbiases
topgenbiases = visbiases
save(mnistpo, hidtop, toprecbiases, topgenbiases)

backprop.run()

