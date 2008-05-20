#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import math
import time
import pprint

import numpy as np
from numpy import matlib
from numpy import random

VERBOSE = 1

def debug(message):
    if VERBOSE > 1:
        print "DEBUG:", message
def info(message):
    if VERBOSE > 0:
        print "INFO:", message

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    import traceback
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print "Locals by frame, innermost last"
    for frame in stack:
        print
        print "Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items():
            print "\t%20s = " % key,
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"


def stats(patterns):
    return "\n".join(["patterns = %s" % len(patterns),
                      "features = %s" % len(patterns[0][0]),
                      "targets  = %s" % len(patterns[0][1])])


def trace(s, sep='-'):
    s = (" %s " % s).center(70, sep)
    row = sep*len(s)
    info("\n".join([row, s, row]))


def assertEqual(a, b, message=None):
    """
    Verbose assertEqual
    """
    if not message:
        message = "Was supposed %s == %s" % (a, b)
    if a != b:
        raise ValueError(message)

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))
def sigmoid_deriv(v):
    return np.multiply(v, (1.0 - v))


class Layer:
    def __init__(self, n_in, n_out, linear=False):
        self.n_in = n_in
        self.n_out = n_out
        self.linear = linear
        self.inputs = None
        self.delta_inputs = None
        self.weights = np.mat(np.random.randn(n_in, n_out)*0.1)
        self.outputs = None
        self.delta_outputs = None
        self.targets = None
        self.errors = None
    def propagate(self, inputs):
        self.inputs = inputs
        #debug("inputs = %s\nweights = %s" % (self.inputs, self.weights))
        self.outputs = sigmoid(self.inputs*self.weights)
        #debug("outputs = %s" % self.outputs)
        return self.outputs
    def backPropagate(self, targets=None, delta_outputs=None):
        if targets != None:
            self.targets = targets
            #debug("targets = %s\noutputs = %s" % (self.targets, self.outputs))
            self.delta_outputs = np.multiply(sigmoid_deriv(self.outputs), (self.targets - self.outputs))
            #debug("delta_outputs = %s" % self.delta_outputs)
            self.errors = np.sum(np.mat(np.array(self.targets - self.outputs)**2), axis=1)
            #debug("errors = %s" % self.errors)
        elif delta_outputs != None:
            self.delta_outputs = delta_outputs
            #debug("delta_outputs = %s" % self.delta_outputs)
        else:
            raise ValueError("provide 'targets' or 'delta_outputs'")
        #debug("inputs = %s\ndelta_outputs = %s\nweights.T = %s" % (self.inputs, self.delta_outputs, self.weights.T))
        self.delta_inputs = np.multiply(sigmoid_deriv(self.inputs), (self.delta_outputs * self.weights.T))
        #debug("delta_inputs = %s\nerrors = %s" % (self.delta_inputs, self.errors))
        return self.delta_inputs
    def updateWeights(self, learn):
        #debug("inputs.T = %s\ndelta_outputs = %s" % (self.inputs.T, self.delta_outputs))
        self.weights += learn * (self.inputs.T * self.delta_outputs)
        #debug("weights = %s" % (self.weights))
        return self.weights
    def __repr__(self):
        return "<Layer %d %d>" % (self.n_in, self.n_out)


class ShallowNetwork:
    def __init__(self, n_in, n_hid, n_out, bias=True):
        self.idx = 1
        self.bias = bias
        if bias:
            n_in = n_in + 1
        random.seed(123)
        self.in_layer = Layer(n_in, n_hid)
        self.out_layer = Layer(n_hid, n_out)
    def propagate(self, inputs):
        if self.bias:
            inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis=1)
        #debug(" propagate IN ".center(70, "-"))
        hiddens = self.in_layer.propagate(inputs)
        #debug(" propagate OUT ".center(70, "-"))
        outputs = self.out_layer.propagate(hiddens)
        return outputs
    def backPropagate(self, targets):
        #debug(" backPropagate OUT ".center(70, "-"))
        delta_inputs = self.out_layer.backPropagate(targets=targets)
        #debug(" backPropagate IN ".center(70, "-"))
        self.in_layer.backPropagate(delta_outputs=delta_inputs)
        return self.out_layer.errors
    def updateWeights(self, learn):
        #debug(" updateWeights IN ".center(70, "-"))
        self.in_layer.updateWeights(learn)
        #debug(" updateWeights OUT ".center(70, "-"))
        self.out_layer.updateWeights(learn)
    def train(self, patterns, iterations=1000, learn=0.05):
        info(" TRAIN ".center(70, "#"))
        for k in range(iterations):
            random.shuffle(patterns)
            error = 0.0
            for i in range(patterns.shape[0]):
                self.propagate(patterns[:,:-self.idx])
                error += self.backPropagate(patterns[:,-self.idx:])
                self.updateWeights(learn)
            if not k % (1+iterations/100):
                info("iter(%s) error = %s" % (iterations - k, error))
    def test(self, patterns):
        info(" TEST ".center(70, "#"))
        for i in range(patterns.shape[0]):
            info("%s -> %s (%s)" % (patterns[i,:-self.idx], self.propagate(patterns[i,:-self.idx]), patterns[i,-self.idx:]))
    def dump(self):
        return {"ShallowNetwork": [self.in_layer, self.out_layer]}
    def __str__(self):
        return "<ShallowNetwork %s>" % str([self.in_layer, self.out_layer])

"""
class DeepNetwork:
    def __init__(self, n_nodes, auto_mode="step"):
        n_nodes[0] += 1 # bias
        self.layers = [Layer(n_in, n_out) for n_in, n_out in zip(n_nodes[:-1], n_nodes[1:])]
        self.auto_mode = auto_mode
    def _connect(self):
        for i in range(len(self.layers)-1):
            self.layers[i].connect(self.layers[i+1])
    def propagate(self, inputs):
        self.layers[0].propagate(inputs)
        for layer in self.layers[1:]:
            layer.propagate()
    def backPropagate(self, targets):
        err = self.layers[-1].backPropagate(targets)
        for layer in reversed(self.layers[:-1]):
            layer.backPropagate()
        return err
    def updateWeights(self, learn):
        for layer in self.layers:
            layer.updateWeights(learn)
    def getOutputs(self, inputs):
        self.propagate(inputs)
        return self.layers[-1].getOutputs()
    def prepare(self, patterns, iterations, learn):
        auto_patterns = [(vector(list(inputs) + [1.0]), vector(list(inputs) + [1.0])) for inputs, targets in patterns]
        info("prepare")
        earlystop = int(0.7 * iterations / len(self.layers))
        for c, layer in enumerate(self.layers):
            if self.auto_mode == "step":
                auto_net = Shallownp.twork(len(layer.getInputs()), len(layer.getOutputs()), len(layer.getInputs()), bias=False)
                #debug("auto_net(step): %s" % auto_net)
                auto_net.in_layer.copyWeights(layer)
                auto_net.train(auto_patterns, iterations - (c * earlystop), 2 * learn * (len(self.layers) - c))
            else:
                auto_net = Shallownp.twork(len(layer.getInputs()), len(layer.getOutputs()), len(self.layers[0].getInputs()), bias=False)
                #debug("auto_net(input): %s" % auto_net)
                auto_net.in_layer.copyWeights(layer)
                auto_net.train(auto_patterns, iterations, learn)
            layer.copyWeights(auto_net.in_layer)
            if layer != self.layers[-1]:
                new_auto_patterns = []
                for inputs, targets in auto_patterns:
                    auto_net.propagate(inputs)
                    new_inputs = auto_net.out_layer.getInputs()
                    if self.auto_mode == "step":
                        new_auto_patterns.append((new_inputs, new_inputs))
                    else:
                        new_auto_patterns.append((new_inputs, targets))
                auto_patterns = new_auto_patterns
            else:
                auto_outputs = []
                for c, (inputs, targets) in enumerate(auto_patterns):
                    auto_net.propagate(inputs)
                    outputs = auto_net.out_layer.getInputs()
                    auto_outputs.append((outputs, patterns[c][1]))
                import pprint
                open("auto_outputs.log", "w+").write(pprint.pformat(auto_outputs)+"\n")
        self._connect()
    def train(self, patterns, iterations=1000, learn=0.05):
        error = last_error = 0.0
        min_error = [float("inf"), [], 0] # err, weights, count
        #self.prepare(patterns, iterations, learn)
        info("train")
        count = iterations
        step = 10 + int(math.log(iterations))
        err = learn/(iterations/10)
        train_patterns = [(vector(list(inputs) + [1.0]), targets) for inputs, targets in patterns]
        while count > 0:
            random.shuffle(train_patterns)
            count -= 1
            last_error = error
            error = 0.0
            for inputs, targets in train_patterns:
                self.propagate(inputs)
                error += self.backPropagate(targets)
                self.updateWeights(learn)
            if not count % step:
                #debug("iter(%s) error = %f" % (count, error))
            if error < min_error[0]:
                min_error = [error, [l.getWeights() for l in self.layers], 0]
            else:
                min_error[2] += 1
                if min_error[2] > 10 *  step:
                    print "Revert to best so far!!"
                    min_error[0] = float("inf")
                    min_error[2] = 0
                    for c, w in enumerate(min_error[1]):
                        self.layers[c].setWeights(w)
            if False and abs(error - last_error) < learn / (iterations * len(patterns)):
                print "early exit, delta_error too small!!"
                break
            if error == nan:
                raise ValueError(error)
    def test(self, patterns):
        def getId(targets):
            if len(targets) > 1:
                return targets.argmax()
            else:
                return int(targets[0] > 0.5) # only Sigmoid...
        res = {}
        test_patterns = [(vector(list(inputs) + [1.0]), targets) for inputs, targets in patterns]
        printed = 0
        for inputs, targets in test_patterns:
            outputs = self.getOutputs(inputs)
            idx = getId(targets)
            res.setdefault(idx, {True: 0.0, False: 0.0})
            res[idx][idx == getId(outputs)] += 1.0
            res[idx]["acc"] = 100 * res[idx][True] / (res[idx][True] + res[idx][False])
            if printed < 10:
                info("%s -> %s" % (outputs, targets))
                printed += 1
        info(pprint.pformat(res))
    def dump(self):
        return {"DeepNetwork": [l.dump() for l in self.layers]}
    def __str__(self):
        return "<DeepNetwork %s>" % str(self.layers)

"""
def demo(iterations=1000, learn=0.05):
    # Teach network XOR function
    patterns = np.mat([[0.0,0.0, 0.0],
                       [0.0,1.0, 1.0],
                       [1.0,0.0, 1.0],
                       [1.0,1.0, 0.0]])

    _patterns = np.mat([[0.0,0.0, 0.0,0.0],
                       [0.0,1.0, 0.0,1.0],
                       [1.0,0.0, 1.0,0.0],
                       [1.0,1.0, 1.0,1.0]])

    # create a network
    net = ShallowNetwork(2, 5, 1)
    #net = DeepNetwork([2, 3, 3, 1], ["step", "input"][0])
    # train it with some patterns
    #for i in range(1):
    #    net.prepare(patterns, 50000, 0.05)
    # test it
    #print net.dump()
    #net.test(patterns)
    print net
    net.train(patterns, iterations, learn)
    net.test(patterns)


if __name__ == "__main__":
    if __debug__:
        import doctest
        doctest.testmod()
    try:
        start_time = time.time()
        demo()
        print "Time:", (time.time() - start_time)
    except:
        print_exc_plus()

