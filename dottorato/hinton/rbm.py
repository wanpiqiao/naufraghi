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

def_eps_w  = 0.1 # Learning rate for weights
def_eps_vb = 0.1 # Learning rate for biases of visible units
def_eps_hb = 0.1 # Learning rate for biases of hidden units
weightcost = 0.0002
initial_momentum  = 0.5
final_momentum    = 0.9

def run(maxepoch, numhid, batchdata, linear=False):
    # This program trains Restricted Boltzmann Machine in which
    # visible, binary, stochastic pixels are connected to
    # hidden, binary, stochastic feature detectors using symmetrically
    # weighted connections. Learning is done with 1-step Contrastive Divergence.
    # The program assumes that the following variables are set externally:
    # maxepoch  -- maximum number of epochs
    # numhid    -- number of hidden units
    # batchdata -- the data that is divided into batches (numcases numdims numbatches)
    # restart   -- set to 1 if learning starts from beginning
    # linear    -- default = False == sigmoid

    numbatches, numcases, numdims = shape(batchdata)

    if linear:
        eps_w = def_eps_w / 100
        eps_vb = def_eps_vb / 100
        eps_hb = def_eps_hb / 100
    else:
        eps_w = def_eps_w
        eps_vb = def_eps_vb
        eps_hb = def_eps_hb

    # Initializing symmetric weights and biases.
    weights   = 0.1*random.randn(numdims, numhid)
    bias_hid  = m.zeros((1, numhid))
    bias_vis  = m.zeros((1, numdims))

    poshidprobs = m.zeros((numcases, numhid))
    neghidprobs = m.zeros((numcases, numhid))
    posprods    = m.zeros((numdims, numhid))
    negprods    = m.zeros((numdims, numhid))
    delta_weights  = m.zeros((numdims, numhid))
    delta_bias_hid = m.zeros((1, numhid))
    delta_bias_vis = m.zeros((1, numdims))
    if linear:
        delta_sigma = m.zeros((1, numhid))
    outprobs = zeros((numbatches, numcases, numhid))

    for epoch in range(maxepoch):
        print 'epoch %d' % epoch
        errsum = 0.0
        last_epoch = epoch == maxepoch - 1
        for batch in range(numbatches):
            print 'epoch %d batch %d/%d' % (epoch, batch, numbatches)

            ######### START POSITIVE PHASE ###################################################
            data = mat(batchdata[batch])
            if linear:
                poshidprobs = (data*weights) + tile(bias_hid, (numcases, 1))
            else:
                poshidprobs = 1.0 / (1.0 + exp(-data*weights - tile(bias_hid, (numcases, 1))))
            posprods  = data.T * poshidprobs
            poshidact = sum(poshidprobs)
            posvisact = sum(data)

            ######### END OF POSITIVE PHASE  #################################################
            poshidstates = poshidprobs > random.rand(numcases, numhid) # in place of a data shuffle

            ######### START NEGATIVE PHASE  ##################################################
            negdata = 1.0 / (1.0 + exp(-poshidstates*weights.T - tile(bias_vis, (numcases, 1))))
            if linear:
                neghidprobs = (negdata*weights) + tile(bias_hid, (numcases, 1))
            else:
                neghidprobs = 1.0 / (1.0 + exp(-negdata*weights - tile(bias_hid, (numcases, 1))))
            negprods  = negdata.T * neghidprobs
            neghidact = sum(neghidprobs)
            negvisact = sum(negdata)

            ######### END OF NEGATIVE PHASE ##################################################
            err = sum(sum( array(data-negdata)**2 ))
            errsum = err + errsum

            if epoch > 5:
                momentum = final_momentum
            else:
                momentum = initial_momentum

            ######### UPDATE WEIGHTS AND BIASES ###############################################
            delta_weights  = momentum*delta_weights + \
                                     eps_w*((posprods-negprods)/numcases - weightcost*weights)
            delta_bias_vis = momentum*delta_bias_vis + (eps_vb/numcases)*(posvisact-negvisact)
            delta_bias_hid = momentum*delta_bias_hid + (eps_hb/numcases)*(poshidact-neghidact)

            weights = weights + delta_weights
            bias_vis = bias_vis + delta_bias_vis
            bias_hid = bias_hid + delta_bias_hid

            ################ END OF UPDATES ####################################################
            if last_epoch:
                outprobs[batch] = poshidprobs

        print '### epoch %4d error %6.1f' % (epoch, errsum)
    # Matlab style return...
    return locals()
