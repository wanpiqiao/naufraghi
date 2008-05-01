#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import math
import time
import random

from cbplnn import Layer

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


def print_stats(patterns):
    print "patterns =", len(patterns)
    print "features =", len(patterns[0][0])
    print "targets  =", len(patterns[0][1])


def trace(s, sep='-'):
    s = (" %s " % s).center(70, sep)
    print sep*len(s)
    print s
    print sep*len(s)


def assertEqual(a, b, message=None):
    """
    Verbose assertEqual
    """
    if not message:
        message = "Was supposed %s == %s" % (a, b)
    if a != b:
        raise ValueError(message)


class ShallowNetwork:
    def __init__(self, n_in, n_hid, n_out, bias=True):
        if bias:
            self.bias = [1.0]
        else:
            self.bias = []
        n_in = n_in + len(self.bias)
        random.seed(123)
        self.in_layer = Layer(n_in, n_hid)
        self.out_layer = Layer(n_hid, n_out)
        self.in_layer.connect(self.out_layer)
    def propagate(self, inputs):
        self.in_layer.propagate(inputs + self.bias)
        self.out_layer.propagate()
    def backPropagate(self, targets):
        err = self.out_layer.backPropagate(targets)
        self.in_layer.backPropagate()
        return err
    def updateWeights(self, learn):
        self.in_layer.updateWeights(learn)
        self.out_layer.updateWeights(learn)
    def getOutputs(self, inputs):
        self.propagate(inputs)
        return self.out_layer.getOutputs()
    def train(self, patterns, iterations=1000, learn=0.05):
        for i in range(iterations):
            error = 0.0
            for inputs, targets in patterns:
                self.propagate(inputs)
                error += self.backPropagate(targets)
                self.updateWeights(learn)
            if __debug__:
                if not i % (1+iterations/100):
                    print "iter(%s) error = %f" % (i, error)
            if error < learn:
                break
    def test(self, patterns):
        for inputs, targets in patterns:
            res = self.getOutputs(inputs)
            print inputs, "->", res, "(%s)" % targets


class DeepNetwork:
    def __init__(self, n_nodes, auto_mode="step"):
        n_nodes[0] += 1 # bias
        self.layers = [Layer(n_in, n_out) for n_in, n_out in zip(n_nodes[:-1], n_nodes[1:])]
        self.auto_mode = "step"
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
    def prepare(self, patterns, iterations, learn):
        auto_patterns = [(inputs + [1.0], inputs + [1.0]) for inputs, targets in patterns]
        if __debug__:
            trace("prepare")
        for layer in self.layers:
            if __debug__:
                print "Layer", self.layers.index(layer), layer
            if self.auto_mode == "step":
                auto_net = ShallowNetwork(len(layer.getInputs()), len(layer.getOutputs()), len(layer.getInputs()), bias=False)
            else:
                auto_net = ShallowNetwork(len(layer.getInputs()), len(layer.getOutputs()), len(self.layers[0].getInputs()), bias=False)
            auto_net.train(auto_patterns, iterations, learn)
            layer.setWeights(auto_net.in_layer)
            new_auto_patterns = []
            for inputs, targets in auto_patterns:
                auto_net.propagate(inputs)
                new_inputs = auto_net.out_layer.getInputs()
                if self.auto_mode == "step":
                    new_auto_patterns.append((new_inputs, new_inputs))
                else:
                    new_auto_patterns.append((new_inputs, inputs))
            auto_patterns = new_auto_patterns
        self._connect()
    def train(self, patterns, iterations=1000, learn=0.05):
        self.prepare(patterns, 10+iterations/100, learn)
        if __debug__:
            trace("train")
        count = iterations * len(patterns)
        step = int(math.log(iterations * len(patterns)))
        err = learn/(iterations/10)
        while count > 0:
            count -= len(patterns)
            error = 0.0
            for inputs, targets in patterns:
                self.propagate(inputs + [1.0])
                error += self.backPropagate(targets)
                self.updateWeights(learn)
            if __debug__:
                if not count % step:
                    print "iter(%s) error = %f" % (count, error)
            if error < err:
                break
    def test(self, patterns):
        for inputs, targets in patterns:
            self.propagate(inputs + [1.0])
            res = self.layers[-1].getOutputs()
            print inputs, "->", res, "(%s)" % targets
    def __str__(self):
        return str(map(str, self.layers))


def demo():
    # Teach network XOR function
    patterns = [
        [[0.0,0.0], [0.0]],
        [[0.0,1.0], [1.0]],
        [[1.0,0.0], [1.0]],
        [[1.0,1.0], [0.0]]
    ]

    # create a network
    #net = ShallowNetwork(2, 5, 1)
    net = DeepNetwork([2, 3, 3, 3, 3, 1], ["step", "input"][0])
    # train it with some patterns
    net.train(patterns, 100000)
    # test it
    print net
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

