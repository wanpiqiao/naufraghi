#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

from __future__ import division

import sys
import time

import numpy as N
from numpy import matlib

#TRAIN_DEEP_NETWORK Trains a deep (multi-layer) network using RBMs
#
#   network = train_deep_network(X, layers, finetune)
#   network = train_deep_network(X, layers, 'Backprop', targets);
#
# The function trains a deep multi-layer feedforward network on the 
# data specified in X by training each layer separately using Restricted 
# Boltzmann Machine training. The depth and number of nodes in the network 
# are specified by the vector layers. For instance, if layers is set to 
# [100 50 10], a network is trained with three hidden layers with 
# respectively 100, 50 nodes and 10 nodes. The number of input (visual)
# nodes is determined by the dimensionality of the input data X. The
# network is trained using a greedy approach. The network may be finetuned
# using backpropagation or contrastive wake-sleep by setting finetune. 
# Possible values are 'Backprop', 'WakeSleep', or 'None' (default = 'None').
# The network is returned in the cell-array network.
#

# This file is part of the Matlab Toolbox for Dimensionality Reduction v0.4b.
# The toolbox can be obtained from http://www.cs.unimaas.nl/l.vandermaaten
# You are free to use, change, or redistribute this code in any way you
# want for non-commercial purposes. However, it is appreciated if you 
# maintain the name of the original author.
#
# (C) Laurens van der Maaten
# Maastricht University, 2007

def train_deep_network(origX, layers, finetune=None, targets=None):
    if finetune and not targets:
        raise ValueError("target must be != None with finetune != None")
    
    # Initialize some variables
    num_layers = len(layers)
    network = [None] * len(num_layers)
    X = mat(origX)
    X = X -  N.min(X)
    X = X / N.max(X)
            
    # Learn layer-by-layer to get an initial network configuration
    for i in range(num_layers):
        
        print 'Training layer', i, '...'
        
        # Train current layer
        if i != len(layers) - 1:
            network[i] = train_rbm(X, layers[i], 'sigmoid')
        else:
            if finetune != 'Backprop':
                network[i] = train_rbm(X, layers[i], 'linear')
            else:
                network[i].W = N.mat(N.random.randn(layers[i - 1], layers[i]) * 0.1)
                network[i].bias_upW = matlib.zeros((1, layers[i]))
                network[i].bias_downW = matlib.zeros((1, layers[i - 1]))
                network[i].type = 'linear'
        
        # Transform data using learned weights
        if i != len(layers) - 1:
            X = 1.0 / (1.0 + N.exp(-(X * network[i].W + N.tile(network[i].bias_upW, (N.shape(X, 1), 1)))))

    # Perform finetuning if desired

    if finetune == 'WakeSleep':
        print 'Finetuning the network using the contrastive wake-sleep algorithm...'
        network = wake_sleep(network, origX)
        
    elif finetune == 'Autoencoder':
        print 'Finetuning the autoencoder using backpropagation...'
        for i in range(num_layers):
            network[2 * no_layers + 1 - i] = network[i]
            network[i].W = network[i].W.T
            network[i].bias = network[i].bias_upW.T
            network[2 * no_layers + 1 - i].bias = network[i].bias_downW.T
        network[no_layers + 1].type = 'sigmoid'
        network = backprop(network, origX, origX)
        
    elif finetune == 'Backprop':
        print 'Finetuning the network using backpropagation...'
        for i in range(num_layers):
            network[i].W = network[i].W.T
            network[i].bias = network[i].bias_upW.T
        network = backprop(network, origX, targets)
        
    elif finetune == 'Unsupervised':
        for i in range(num_layers):
            network[i].W = network[i].W.T
            network[i].bias = network[i].bias_upW.T
        
    else:
        pass
        # Do nothing
