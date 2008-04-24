#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import math
import time
import random

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

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

def dot(vec1, vec2):
    """
    Vector dot product
    >>> dot([2,2,2], [1,2,3])
    12
    """
    return sum([x * w for (x, w) in zip(vec1, vec2)])

def _vec(func):
    def __vec(vec1, vec2, out=None):
        if out == None:
            return [func(x, w) for (x, w) in zip(vec1, vec2)]
        else:
            for i in range(len(out)):
                out[i] = func(vec1[i], vec2[i])
            return out
    return __vec

def _map(func):
    def __map(vec, out=None):
        if out == None:
            return map(func, vec)
        else:
            for i in range(len(out)):
                out[i] = func(vec[i])
    return __map

def sigmoid(val):
    return 1.0 / (1.0 + math.exp(-val))
def sigmoid_deriv(val):
    return val * (1.0 - val)
sigmoid.vec = _vec(sigmoid)
sigmoid.map = _map(sigmoid)
sigmoid.deriv = sigmoid_deriv
sigmoid.deriv.vec = _vec(sigmoid_deriv)
sigmoid.deriv.map = _map(sigmoid_deriv)

def qloss(output, target):
    return sigmoid.deriv(output) * (target - output)
qloss.vec = _vec(qloss)

def diff(a, b):
    return a - b
diff.vec = _vec(diff)

def makeMatrix(rows, cols, fill=0.0):
    """
    >>> makeMatrix(2, 3)
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> import random
    >>> random.seed(0)
    >>> makeMatrix(2, 3, random.random)
    [[0.84442185152504812, 0.75795440294030247, 0.420571580830845],\
 [0.25891675029296335, 0.51127472136860852, 0.40493413745041429]]
    """
    def _fill():
        return callable(fill) and fill() or fill
    return [[_fill() for j in range(cols)] for i in range(rows)]

def transposed(matrix):
    """
    Returns the transposed `matrix`
    >>> transposed([[1,2,3], [4,5,6]])
    [(1, 4), (2, 5), (3, 6)]
    """
    return zip(*matrix)

class Layer:
    def __init__(self, n_in, n_out, squash=sigmoid):
        def _rand():
            return rand(-2.0, 2.0)
        self.n_in = range(n_in)
        self.n_out = range(n_out)
        self.squash = squash
        self.inputs = [1.0]*n_in
        self.outputs = [1.0]*n_out # squash(activations)
        self.weights = makeMatrix(n_out, n_in, _rand)
        self.delta_inputs = [0.0]*n_in
        self.delta_outputs = [0.0]*n_out
        self.next = None
        self.prev = None
    def propagate(self, inputs=None):
        if inputs != None:
            if __debug__: assertEqual(len(inputs), len(self.n_in))
            if self.prev == None:
                self.inputs = inputs
            else:
                raise ValueError("Inputs are not allowed in the middle of a chain!!")
        #if __debug__: print "propagate(%s): outputs = %s ->" % (self.inputs, self.outputs),
        for k in self.n_out:
            self.outputs[k] = self.squash(dot(self.weights[k], self.inputs))
        #if __debug__: print "%s" % self.outputs
    def backPropagate(self, targets=None):
        if targets != None:
            if __debug__: assertEqual(len(targets), len(self.n_out))
            if self.next == None:
                self.delta_outputs = qloss.vec(self.outputs, targets)
            else:
                raise ValueError("Targets are not allowed in the middle of a chain!!")
        _weights = transposed(self.weights)
        #if __debug__: print "backPropagate(%s): delta_inputs = %s ->" % (self.delta_outputs, self.delta_inputs),
        for j in self.n_in:
            self.delta_inputs[j] = self.squash.deriv(self.inputs[j]) * dot(_weights[j], self.delta_outputs)
        #if __debug__: print "%s" % self.delta_inputs
    def updateWeights(self, learn):
        # locals for performance or traceback
        # weights, deltas, inputs = self.weights, self.delta_inputs, self.inputs
        for j in self.n_in:
            for k in self.n_out:
                self.weights[k][j] += learn * self.delta_outputs[k] * self.inputs[j]
    def connect(self, next):
        if __debug__: assertEqual(len(self.outputs), len(next.inputs))
        self.next = next
        next.prev = self
        next.inputs = self.outputs
        next.delta_inputs = self.delta_outputs
    def graphviz(self):
        res = ["digraph Layer {", "rankdir = LR;"]
        res += [" subgraph Layer_in {"] + [" " + " ".join(["I%s" % i for i in range(len(self.inputs))]) + ";"] + [" }"]
        res += [" subgraph Layer_out {"] + [" " + " ".join(["O%s" % j for j in range(len(self.outputs))]) + ";"] + [" }"]
        for i, input in enumerate(self.inputs):
            for j, output in enumerate(self.outputs):
                _w = "%s -> %s [label = %f];" % ("I%s" % i, "O%s" % j, self.weights[j][i])
                res.append(_w)
        return "\n".join(res + ["}"])
    def __str__(self):
        return "<Layer(%s, %s, %s)>" % (len(self.n_in), len(self.n_out), self.squash.__name__)


class ShallowNetwork:
    def __init__(self, n_in, n_hid, n_out, bias=True):
        if bias:
            self.bias = [1.0]
        else:
            self.bias = []
        n_in = n_in + len(self.bias)
        self.in_layer = Layer(n_in, n_hid)
        self.out_layer = Layer(n_hid, n_out)
        self.in_layer.connect(self.out_layer)
    def _propagate(self, inputs):
        self.in_layer.propagate(inputs + self.bias)
        self.out_layer.propagate()
    def _backPropagate(self, targets, learn):
        self.out_layer.backPropagate(targets)
        self.in_layer.backPropagate()
        self.in_layer.updateWeights(learn)
        self.out_layer.updateWeights(learn)
    def train(self, patterns, iterations=1000, learn=0.05):
        def sq2(x):
            return 0.5 * x**2
        for i in range(iterations):
            error = 0.0
            for inputs, targets in patterns:
                self._propagate(inputs)
                self._backPropagate(targets, learn)
                error += sum(map(sq2, diff.vec(self.out_layer.outputs, targets)))
            if __debug__:
                if not i % 100:
                    print "iter(%s) error = %f" % (i, error)
            if error < learn:
                break
    def test(self, patterns):
        for inputs, targets in patterns:
            self._propagate(inputs)
            res = self.out_layer.outputs
            print inputs, "->", res, "(%s)" % targets


class DeepNetwork:
    def __init__(self, n_nodes, auto_mode="step"):
        n_nodes[0] += 1 # bias
        self.layers = [Layer(n_in, n_out) for n_in, n_out in zip(n_nodes[:-1], n_nodes[1:])]
        self.auto_mode = "step"
    def _connect(self):
        for i in range(len(self.layers)-1):
            self.layers[i].connect(self.layers[i+1])
    def _propagate(self, inputs):
        self.layers[0].propagate(inputs)
        for layer in self.layers[1:]:
            layer.propagate()
    def _backPropagate(self, targets, learn):
        self.layers[-1].backPropagate(targets)
        for layer in reversed(self.layers[:-1]):
            layer.backPropagate()
        for layer in self.layers:
            layer.updateWeights(learn)
    def _prepare(self, patterns, iterations, learn):
        auto_patterns = [(inputs + [1.0], inputs + [1.0]) for inputs, targets in patterns]
        if __debug__:
            trace("_prepare")
        for layer in self.layers:
            if __debug__:
                print "Layer", self.layers.index(layer), layer
            if self.auto_mode == "step":
                auto_net = ShallowNetwork(len(layer.inputs), len(layer.outputs), len(layer.inputs), bias=False)
            else:
                auto_net = ShallowNetwork(len(layer.inputs), len(layer.outputs), len(self.layers[0].inputs), bias=False)
            auto_net.train(auto_patterns, iterations, learn)
            layer.weights = auto_net.in_layer.weights
            new_auto_patterns = []
            for inputs, targets in auto_patterns:
                auto_net._propagate(inputs)
                new_inputs = auto_net.out_layer.inputs
                if self.auto_mode == "step":
                    new_auto_patterns.append((new_inputs, new_inputs))
                else:
                    new_auto_patterns.append((new_inputs, inputs))
            auto_patterns = new_auto_patterns
        self._connect()
    def train(self, patterns, iterations=1000, learn=0.05):
        self._prepare(patterns, iterations/10, learn)
        if __debug__:
            trace("train")
        def sq2(x):
            return 0.5 * x**2
        count = iterations
        last_error = None
        while count:
            count -= 1
            error = 0.0
            for inputs, targets in patterns:
                self._propagate(inputs + [1.0])
                self._backPropagate(targets, learn)
                error += sum(map(sq2, diff.vec(self.layers[-1].outputs, targets)))
            if __debug__:
                if not count % (100 * int(math.log(iterations))):
                    print "iter(%s) error = %f, delta = %f" % (count, error, abs(error - last_error) * 100)
            if count != iterations-1:
                if error < learn:
                    break
                if abs(error - last_error) > learn/iterations:
                    count += 42
            last_error = error
    def test(self, patterns):
        for inputs, targets in patterns:
            self._propagate(inputs + [1.0])
            res = self.layers[-1].outputs
            print inputs, "->", res, "(%s)" % targets
    def __str__(self):
        return str(map(str, self.layers))


def demo():
    # Teach network XOR function
    patterns = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network
    #net = ShallowNetwork(2, 5, 1)
    net = DeepNetwork([2, 3, 3, 3, 3, 1], ["step", "input"][0])
    # train it with some patterns
    net.train(patterns, 10000)
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

