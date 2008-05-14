#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import time

from numpy import *
import numpy.matlib as m

# Version 1.000 
#
# Code provided by Geoff Hinton and Ruslan Salakhutdinov 
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

def run():
    # Matlab style input...
    locals().update(globals())
    # This program trains Restricted Boltzmann Machine in which
    # visible, binary, stochastic pixels are connected to
    # hidden, stochastic real-valued feature detectors drawn from a unit
    # variance Gaussian whose mean is determined by the input from 
    # the logistic visible units. Learning is done with 1-step Contrastive Divergence.
    # The program assumes that the following variables are set externally:
    # maxepoch  -- maximum number of epochs
    # numhid    -- number of hidden units
    # batchdata -- the data that is divided into batches (numcases numdims numbatches)
    # restart   -- set to 1 if learning starts from beginning

    epsilonw    = 0.001   # Learning rate for weights 
    epsilonvb   = 0.001   # Learning rate for biases of visible units
    epsilonhb   = 0.001   # Learning rate for biases of hidden units 
    weightcost  = 0.0002 
    initialmomentum  = 0.5
    finalmomentum    = 0.9

    numcases, numdims, numbatches = shape(batchdata)

    if restart == 1:
        restart = 0
        epoch = 0

        # Initializing symmetric weights and biases. 
        vishid     = 0.1*random.randn(numdims, numhid)
        hidbiases  = m.zeros((1, numhid))
        visbiases  = m.zeros((1, numdims))

        poshidprobs = m.zeros((numcases, numhid))
        neghidprobs = m.zeros((numcases, numhid))
        posprods    = m.zeros((numdims, numhid))
        negprods    = m.zeros((numdims, numhid))
        vishidinc  = m.zeros((numdims, numhid))
        hidbiasinc = m.zeros((1, numhid))
        visbiasinc = m.zeros((1, numdims))
        sigmainc = m.zeros((1, numhid))
        batchposhidprobs = zeros((numcases, numhid, numbatches))

    for epoch in range(epoch, maxepoch):
        print 'epoch %d\n' % epoch 
        errsum = 0
        for batch in range(0, numbatches)
            print 'epoch %d batch %d\n' % (epoch, batch) 

            ######### START POSITIVE PHASE ###################################################
            data = mat(batchdata[:,:,batch])
            poshidprobs = (data*vishid) + tile(hidbiases, (numcases, 1)) 
            batchposhidprobs[:,:,batch] = poshidprobs
            posprods    = data.T * poshidprobs
            poshidact   = sum(poshidprobs)
            posvisact = sum(data)

            ######### END OF POSITIVE PHASE  #################################################
            poshidstates = poshidprobs > random.rand(numcases, numhid);

            ######### START NEGATIVE PHASE  ##################################################
            negdata = 1.0 / (1.0 + exp(-poshidstates*vishid.T - tile(visbiases, (numcases, 1))))
            neghidprobs = (negdata*vishid) + tile(hidbiases, (numcases, 1))
            negprods  = negdata.T*neghidprobs
            neghidact = sum(neghidprobs)
            negvisact = sum(negdata)

            ######### END OF NEGATIVE PHASE ##################################################
            err = sum(sum( (data-negdata)**2 ))
            errsum = err + errsum

            if epoch > 5:
                momentum = finalmomentum
            else:
                momentum = initialmomentum

            ######### UPDATE WEIGHTS AND BIASES ############################################### 
            vishidinc = momentum*vishidinc + \
                        epsilonw*( (posprods-negprods)/numcases - weightcost*vishid)
            visbiasinc = momentum*visbiasinc + (epsilonvb/numcases)*(posvisact-negvisact)
            hidbiasinc = momentum*hidbiasinc + (epsilonhb/numcases)*(poshidact-neghidact)

            vishid = vishid + vishidinc
            visbiases = visbiases + visbiasinc
            hidbiases = hidbiases + hidbiasinc

            ################ END OF UPDATES #################################################### 

      print 'epoch %4d error %6.1f  \n' % (epoch, errsum)
    # Matlab style return...
    globals().update(locals())

