# Copyright (C) 2008 Matteo Bertini

import random

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t 
    void free(void *ptr)
    void *malloc(size_t size)
    void *realloc(void *ptr, size_t size)
    size_t strlen(char *s)
    char *strcpy(char *dest, char *src)
    int rand()

cdef extern from "math.h":
    double exp(double theta)
    double tanh(double theta)
    double pow(double base, double exponent)
    double log(double x)

# Squash functions ######################################

cdef class Squasher:
    cpdef double func(self, double val):
        return 0.0
    cpdef double deriv(self, double val):
        return 1.0

cdef class Linear(Squasher):
    cpdef double func(self, double val):
        return val
    cpdef double deriv(self, double val):
        return 1.0

cdef class Hyperbolic(Squasher):
    cpdef double unc(self, double val):
        return 1.7159 * tanh(val * 2.0 / 3.0) # f(1) = 1 and f(-1) = -1
    cpdef double deriv(self, double val):
        return 1 - pow(tanh(val * 2.0 / 3.0), 2.0)

cdef class Sigmoid(Squasher):
    cpdef double func(self, double val):
        return 1.0 / (1.0 + exp(-val))
    cpdef double deriv(self, double val):
        return val * (1.0 - val)

# FIXME, find an interface to integrate the softmax actiovation
cdef double* softmax(double* outputs, double* targets, int num):
    cdef double* prob = <double *>malloc(num * sizeof(double))
    cdef double _max = 0.0
    for k from 0 <= k < num: # use max(outputs) to avoid overflow
        if outputs[k] > _max:
            _max = outputs[k]
    cdef double den = 0.0
    for k from 0 <= k < num:
        den += exp(outputs[k] - _max)
    for k from 0 <= k < num:
        prob[k] = exp(outputs[k] - _max) / den
    return prob

# Loss functions #######################################
# 5.2 PRML Bishop

cdef class Loss:
    cdef Squasher squash
    def __init__(self, squash):
        self.squash = squash()
    cpdef double deriv(self, double output, double target):
        return 0.0
    cdef double error(self, double* outputs, double* targets, int num):
        return 0.0

cdef class SumOfSquares(Loss):
    def __init__(self, squash=Linear):
        Loss.__init__(self, squash)
    cpdef double deriv(self, double output, double target):
        return self.squash.deriv(output) * (target - output)
    cdef double error(self, double* outputs, double* targets, int num):
        cdef double _error = 0.0
        for k from 0 <= k < num:
            _error += (outputs[k] - targets[k]) * (outputs[k] - targets[k])
        return 0.5 * _error

cdef class CrossEntropy(Loss):
    def __init__(self, squash=Sigmoid):
        Loss.__init__(self, squash)
    cpdef double deriv(self, double output, double target):
        return self.squash.deriv(output) * (target - output)
    cdef double error(self, double* outputs, double* targets, int num):
        cdef double _error = 0.0
        for k from 0 <= k < num:
            _error += targets[k]*log(outputs[k]) + (1.0 - targets[k])*log(1.0 - outputs[k])
        return - _error

# Matrix / Vector functions #######################################

cdef class Vector:
    cdef int size
    cdef double* data
    def __new__(self, array):
        self.size = len(array)
        self.data = <double *>malloc(self.size * sizeof(double))
        for i, val in enumerate(array):
            self.data[i] = val
    cdef double get(self, int idx):
        return self.data[idx]
    cdef set(self, int idx, double val):
        self.data[idx] = val
    def __getitem__(self, int idx):
        assert 0 <= idx < self.size, "Index Error: %d" % idx
        return self.data[idx]
    def __setitem__(self, int idx, double val):
        assert 0 <= idx < self.size, "Index Error: %d" % idx
        self.data[idx] = val
    def __len__(self):
        return self.size
    def __repr__(self):
        return "Vector(%s)" % [self.data[i] for i in range(self.size)]
    def __dealloc__(self):
        free(self.data)

cdef double dot(double* vec1, double* vec2, int num):
    cdef double _sum = 0.0
    for i from 0 <= i < num:
        _sum += vec1[i] * vec2[i]
    return _sum

cdef double dot_t(double** matrix, int j, double* vec, int num):
    cdef double _sum = 0.0
    for k from 0 <= k < num:
        _sum += matrix[k][j] * vec[k]
    return _sum

# Layer class #####################################################

cdef class Layer:
    cdef int n_in
    cdef int n_out
    cdef double* inputs
    cdef double* delta_inputs
    cdef double** weights
    cdef double* outputs
    cdef double* delta_outputs
    cdef double* targets
    cdef Loss loss
    cdef int connected
    def __new__(self, int n_in, int n_out, loss=CrossEntropy, squash=None):
        self.n_in = n_in
        self.n_out = n_out
        self.inputs = <double *>malloc(n_in * sizeof(double))
        self.delta_inputs = <double *>malloc(n_in * sizeof(double))
        self.weights = <double **>malloc(n_out * sizeof(double*))
        for k from 0 <= k < n_out:
            self.weights[k] = <double *>malloc(n_in * sizeof(double))
        self.outputs = <double *>malloc(n_out * sizeof(double))
        self.delta_outputs = <double *>malloc(n_out * sizeof(double))
        self.targets = <double *>malloc(n_out * sizeof(double))
        if not squash:
            self.loss = loss()
        else:
            self.loss = loss(squash)
        self._init_values()
        self.connected = 0
    cdef _init_values(self):
        for j from 0 <= j < self.n_in:
            self.inputs[j] = 1.0
            self.delta_inputs[j] = 0.0
        for k from 0 <= k < self.n_out:
            for j from 0 <= j < self.n_in:
                self.weights[k][j] = random.uniform(-2, 2)
            self.outputs[k] = 1.0
            self.delta_outputs[k] = 0.0
            self.targets[k] = 1.0
    def propagate(self, inputs=None):
        if inputs != None:
            for j from 0 <= j < self.n_in:
                self.inputs[j] = inputs[j]
        self._propagate()
    cdef _propagate(self):
        for k from 0 <= k < self.n_out:
            self.outputs[k] = self.loss.squash.func(dot(self.weights[k], self.inputs, self.n_in))
    def backPropagate(self, targets=None):
        if targets != None:
            for k from 0 <= k < self.n_out:
                self.targets[k] = targets[k]
                self.delta_outputs[k] = self.loss.deriv(self.outputs[k], self.targets[k])
        self._backPropagate()
        if targets != None:
            return self.error()
    cdef _backPropagate(self):
        for j from 0 <= j < self.n_in:
            self.delta_inputs[j] = self.loss.squash.deriv(self.inputs[j]) * dot_t(self.weights, j, self.delta_outputs, self.n_out)
    cpdef error(self):
        return self.loss.error(self.outputs, self.targets, self.n_out)
    cpdef updateWeights(self, double learn):
        cdef double momentum = 1.0
        for j from 0 <= j < self.n_in:
            for k from 0 <= k < self.n_out:
                self.weights[k][j] += (0.5 + (rand() % 100) / 100.0) * learn * (self.delta_outputs[k] * self.inputs[j])
    cpdef connect(self, Layer next):
        next.connected = 1
        next.inputs = self.outputs
        next.delta_inputs = self.delta_outputs
    cpdef copyWeights(self, Layer other):
        for j from 0 <= j < self.n_in:
            for k from 0 <= k < self.n_out:
                self.weights[k][j] = other.weights[k][j]
    def getInputs(self):
        res = []
        for j from 0 <= j < self.n_in:
            res.append(self.inputs[j])
        return res
    def getWeights(self):
        res = []
        for k from 0 <= k < self.n_out:
            res.append([])
            for j from 0 <= j < self.n_in:
                res[k].append(self.weights[k][j])
        return res
    def setWeights(self, weights):
        for k from 0 <= k < self.n_out:
            for j from 0 <= j < self.n_in:
                self.weights[k][j] = weights[k][j]
    def getOutputs(self, inputs=None):
        if inputs != None:
            self.propagate(inputs)
        res = []
        for k from 0 <= k < self.n_out:
            res.append(self.outputs[k])
        return res
    def dump(self):
        res = dict(inputs  = self.getInputs(),
                   weights = self.getWeights(),
                   outputs = self.getOutputs())
        return {"Layer": res}
    def __repr__(self):
        return "<Layer %d %d>" % (self.n_in, self.n_out)
    def __dealloc__(self):
        if not self.connected:
            free(self.inputs)
            free(self.delta_inputs)
        for k from 0 <= k < self.n_out:
            free(self.weights[k])
        free(self.weights)
        free(self.outputs)
        free(self.delta_outputs)
        free(self.targets)


