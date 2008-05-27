#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

from __future__ import division

import sys
import time

import numpy as N
from numpy import matlib

#TRAIN_RBM Trains a Restricted Boltzmann Machine using contrastive divergence
#
#   machine = train_rbm(X, h, squash, epsilon, max_i)
#
# Trains a first-order Restricted Boltzmann Machine on dataset X. The RBM
# has h hidden nodes (default = 20). The training is performed by means of
# the contrastive divergence algorithm. The activation function that
# is applied in the hidden layer is specified by squash. Possible values are
# 'linear' and 'sigmoid' (default = 'sigmoid'). In the training of the RBM,
# the learning rate is determined by epsilon (default = 0.25). The maximum
# number of iations can be specified through max_i (default = 50).
# The trained RBM is returned in the machine struct.
#
# A Boltzmann Machine is a graphical model which in which every node is
# connected to all other nodes, except to itself. The nodes are binary,
# i.e., they have either value -1 or 1. The model is similar to Hopfield
# networks, except for that its nodes are stochastic, using a logistic
# distribution. It can be shown that the Boltzmann Machine can be trained by
# means of an extremely simple update rule. However, training is in
# practice not feasible.
#
# In a Restricted Boltzmann Machine, the nodes are separated into visible
# and hidden nodes. The visible nodes are not connected to each other, and
# neither are the hidden nodes. When training an RBM, the same update rule
# can be used, however, the data is now clamped onto the visible nodes.
# This training procedure is called contrastive divergence. Alternatively,
# the visible nodes may be Gaussians instead of binary logistic nodes.
#

# This file is part of the Matlab Toolbox for Dimensionality Reduction v0.4b.
# The toolbox can be obtained from http://www.cs.unimaas.nl/l.vandermaaten
# You are free to use, change, or redistribute this code in any way you
# want for non-commercial purposes. However, it is appreciated if you
# maintain the name of the original author.
#
# (C) Laurens van der Maaten
# Maastricht University, 2007

class RBM:
    pass

def train_rbm(X, numhid=20, squash='sigmoid', epsilon=0.1, max_iter=100):

    # Important parameters
    initial_momentum = 0.5     # momentum for first five iations
    final_momentum = 0.9       # momentum for remaining iations
    weight_cost = 0.0002       # costs of weight update

    # Initialize some variables
    n, v = shape(X)
    batch_size = 1 + round(n / 20) # numbatches... tune it for you system/dataset
    W = N.mat(N.random.randn(v, numhid) * 0.1)
    bias_hid = matlib.zeros((1, numhid)
    bias_vis = matlib.zeros((1, v))
    deltaW = matlib.zeros((v, numhid))
    deltaBias_hid = matlib.zeros((1, numhid))
    deltaBias_vis = matlib.zeros((1, v))

    # Main loop
    for i in range(max_iter):

        # Print progress
        if i % 10 == 0:
            print 'Iteration ', i, '...'

        # Set momentum
        if i <= 5:
            momentum = initial_momentum
        else:
            momentum = final_momentum

        # Run for all mini-batches (= Gibbs sampling step 0)
        ind = N.random.shuffle(arange(n))
        for batch in range(0, n, batch_size):

            if batch + batch_size <= n:

                # Set values of visible nodes (= Gibbs sampling step 0)
                data = X[ind[batch:batch + batch_size]]

                # Compute probabilities for hidden nodes (= Gibbs sampling step 0)
                if squash == 'sigmoid':
                    poshidprobs = 1.0 / (1.0 + N.exp(-(data * W + N.tile(bias_hid, (batch_size, 1)))))
                else:
                    poshidprobs = data * W + N.tile(bias_hid, (batch_size, 1))

                # Hinton avoids shuffle but propagate the states:
                # poshidstates = poshidprobs > N.random.rand(numcases, numhid)
                # replacing poshidprobs with poshidstates in negdata

                # Compute probabilities for visible nodes (= Gibbs sampling step 1)
                negdata = 1.0 / (1.0 + N.exp(-(poshidprobs * W.T + N.tile(bias_vis, (batch_size, 1)))))

                # Compute probabilities for hidden nodes (= Gibbs sampling step 1)
                if squash == 'sigmoid':
                    neghidprobs = 1.0 / (1.0 + N.exp(-(negdata * W + N.tile(bias_hid, (batch_size, 1)))))
                else:
                    neghidprobs = negdata * W + N.tile(bias_hid, (batch_size. 1))

                # Now compute the weights update (= contrastive divergence)
                posprods = poshidprobs.T * data    # one can also swap the product and
                negprods = neghidprobs.T * negdata # remove the traspose here --------------\/
                deltaW = momentum * deltaW + (epsilon / batch_size) * ((posprods - negprods).T - (weight_cost * W))
                deltaBias_hid = momentum * deltaBias_hid + (epsilon / batch_size) * (N.sum(poshidprobs, 1) - N.sum(neghidprobs, 1))
                deltaBias_vis = momentum * deltaBias_vis + (epsilon / batch_size) * (N.sum(data, 1) - N.sum(negdata, 1))

                # Divide by number of elements for linear activations
                if squash != 'sigmoid':
                    deltaW        = deltaW        ./ (v * numhid)
                    deltaBias_hid = deltaBias_hid ./ numhid
                    deltaBias_vis = deltaBias_vis ./ v

                # Update the network weights
                W         = W        + deltaW
                bias_hid  = bias_hid + deltaBias_hid
                bias_vis  = bias_vis + deltaBias_vis

    # Return RBM
    machine = RBM()
    machine.W = W
    machine.bias_hid = bias_hid
    machine.bias_vis = bias_vis
    machine.squash = squash
    machine.tied = 'yes'

    return machine
