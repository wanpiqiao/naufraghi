#!/usr/bin/env python
"""
    Translator Demo

    Run this file -- over regular Python! -- to analyse and type-annotate
    the functions and class defined in this module, starting from the
    entry point function demo().

    Requires Pygame.
"""
# Back-Propagation Neural Networks
# 
# Written in Python.  See http://www.python.org/
#
# Neil Schemenauer <nascheme@enme.ucalgary.ca>
#
# Modifications to the original (Armin Rigo):
#   * import random from PyPy's lib, which is Python 2.2's plain
#     Python implementation
#   * starts the Translator instead of the demo by default.

import sys
import math
import time

import autopath
from pypy.rlib import rrandom

PRINT_IT = False

random = rrandom.Random(1)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(rows, cols, fill=0.0):
    return [[fill]*cols for i in range(rows)]

def randomizeMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = rand(-2.0, 2.0)

def sigmoid(val):
    return 1.0/(1.0+math.exp(-val))
def sigmoid_deriv(val):
    return val * (1.0 - val)
sigmoid.deriv = sigmoid_deriv

def dot(vec1, vec2):
    _sum = 0.0
    for i in range(len(vec1)):
        _sum += vec1[i] * vec2[i]
    return _sum
    #return sum([x * w for (x, w) in zip(vec1, vec2)])

def propagate(inputs, weights, outputs, n_out=None):
    """
    Feed Forward propagation
    IN: inputs, weights, n_out
    IN-OUT: output (modified inplace)
    """
    if not n_out:
        n_out = len(outputs)
    for j in range(n_out):
        _weights = [r[j] for r in weights]
        outputs[j] = sigmoid(dot(inputs, _weights))

class ShallowNetwork:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.n_in = ni + 1 # +1 for bias node
        self.n_hid = nh
        self.n_out = no

        # activations for nodes
        self.inputs = [1.0]*self.n_in
        self.hiddens = [1.0]*self.n_hid
        self.outputs = [1.0]*self.n_out
        
        # create weights
        self.weights_in = makeMatrix(self.n_in, self.n_hid)
        self.weights_hid = makeMatrix(self.n_hid, self.n_out)
        # set them to random values
        randomizeMatrix(self.weights_in)
        randomizeMatrix(self.weights_hid)

        # last change in weights for momentum   
        self.wchange_in = makeMatrix(self.n_in, self.n_hid)
        self.wchange_out = makeMatrix(self.n_hid, self.n_out)

    def propagate(self, inputs):
        if len(inputs) != self.n_in-1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.n_in-1): # let bias out
            #self.inputs[i] = 1.0/(1.0+math.exp(-inputs[i]))
            self.inputs[i] = inputs[i]

        # hidden activations
        propagate(self.inputs, self.weights_in, self.hiddens, self.n_hid)

        # output activations
        propagate(self.hiddens, self.weights_hid, self.outputs, self.n_out)

        return self.outputs[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.n_out:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [0.0] * self.n_out
        for k in range(self.n_out):
            ao = self.outputs[k]
            output_deltas[k] = sigmoid.deriv(ao)*(targets[k]-ao)

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.n_hid
        for j in range(self.n_hid):
            hidden_deltas[j] = sigmoid.deriv(self.hiddens[j]) * dot(output_deltas, self.weights_hid[j])

        # update output weights
        for j in range(self.n_hid):
            for k in range(self.n_out):
                change = output_deltas[k]*self.hiddens[j]
                self.weights_hid[j][k] += N*change + M*self.wchange_out[j][k]
                self.wchange_out[j][k] = change
                #print N*change, M*self.wchange_out[j][k]

        # update input weights
        for i in range(self.n_in):
            for j in range(self.n_hid):
                change = hidden_deltas[j]*self.inputs[i]
                self.weights_in[i][j] += N*change + M*self.wchange_in[i][j]
                self.wchange_in[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            delta = targets[k]-self.outputs[k]
            error += 0.5*delta*delta # delta**2 is not supported
        return error

    def test(self, patterns):
        for p in patterns:
            if PRINT_IT:
                print p[0], '->', self.propagate(p[0]), p[1]

    def weights(self):
        if PRINT_IT:
            print 'Input weights:'
            for i in range(self.n_in):
                print self.weights_in[i]
            print
            print 'Output weights:'
            for j in range(self.n_hid):
                print self.weights_hid[j]

    def train(self, patterns, iterations=2000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.propagate(inputs)
                error = error + self.backPropagate(targets, N, M)
            if PRINT_IT and i % 100 == 0:
                print 'error %f' % error


def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, four hidden, and one output nodes
    n = ShallowNetwork(2, 4, 1)
    # train it with some patterns
    n.train(pat, 2000)
    # test it
    n.test(pat)



if __name__ == '__main__':
    PRINT_IT = True
    demo()
    PRINT_IT = False
    #sys.exit(0)
    
    print 'Loading...'
    from pypy.translator.interactive import Translation
    t = Translation(demo)
    
    print 'Annotating...'
    t.annotate([])
    t.viewcg()

    print 'Specializing...'
    t.rtype()   # enable this to see (some) lower-level Cish operations
    
    print 'Compiling...'
    f = t.compile_c()

    print 'Running...'
    T = time.time()
    for i in range(10):
        f()
    t1 = time.time() - T
    print "that took", t1

    T = time.time()
    for i in range(10):
        demo()
    t2 = time.time() - T
    print "compared to", t2
    print "a speed-up of", t2/t1
    
