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

# Matrix / Vector classes ###########################################

cdef class Vector:
    cdef int size
    cdef double* data
    def __new__(self, int size, double fill=0.0):
        self.size = size
        self.data = <double *>malloc(size * sizeof(double))
        for i from 0 <= i < size:
            self.data[i] = fill
    cdef double get(self, int idx):
        return self.data[idx]
    cdef set(self, int idx, double val):
        self.data[idx] = val
    def __getitem__(self, int idx):
        if not 0 <= idx < self.size: raise IndexError
        return self.data[idx]
    def __setitem__(self, int idx, double val):
        if not 0 <= idx < self.size: raise IndexError
        self.data[idx] = val
    cpdef int argmax(self):
        cdef double _max = self.data[0]
        cdef int idx = 0
        for i from 1 <= i < self.size:
            if self.data[i] > _max:
                _max = self.data[i]
                idx = i
        return idx
    cpdef double max(self):
        return self.data[self.argmax()]
    def __len__(self):
        return self.size
    def __repr__(self):
        return "Vector(%s)" % [self.data[i] for i in range(self.size)]
    def __dealloc__(self):
        free(self.data)

def vector(array):
    vec = Vector(len(array))
    for i, v in enumerate(array):
        vec[i] = v
    return vec

cdef class Matrix:
    cdef int rows
    cdef int cols
    cdef double* data
    def __new__(self, int rows, int cols, double fill=0.0):
        self.rows = rows
        self.cols = cols
        self.data = <double *>malloc(rows * cols * sizeof(double))
        for i from 0 <= i < rows * cols:
            self.data[i] = fill
    cpdef double get(self, int row, int col):
        return self.data[(row*self.rows) + col]
    cpdef set(self, int row, int col, double val):
        self.data[(row*self.rows) + col] = val
    def __getitem__(self, int row):
        if not 0 <= row < self.rows: raise IndexError
        return vector([self.get(row, col) for col from 0 <= col < self.cols])
    def __setitem__(self, int row, Vector vals):
        if not 0 <= row < self.rows: raise IndexError
        if not vals.size > self.cols: raise IndexError
        for col from 0 <= col < self.cols:
            self.set(row, col, vals[col])
    def __len__(self):
        return self.rows
    def __repr__(self):
        return "Matrix(%s)" % "\n".join([str(self.__getitem__(i)) for i in range(self.rows)])
    def __dealloc__(self):
        free(self.data)

# Squash functions ######################################

cdef class Squasher:
    cpdef double func(self, Vector activations, int k):
        return 0.0
    cpdef double deriv(self, Vector activations, int k):
        return 1.0

cdef class Linear(Squasher):
    cpdef double func(self, Vector activations, int k):
        return activations[k]
    cpdef double deriv(self, Vector activations, int k):
        return 1.0

cdef class Hyperbolic(Squasher):
    cpdef double func(self, Vector activations, int k):
        return 1.7159 * tanh(activations[k] * 2.0 / 3.0) # f(1) = 1 and f(-1) = -1
    cpdef double deriv(self, Vector activations, int k):
        return 1 - pow(tanh(activations[k] * 2.0 / 3.0), 2.0)

cdef class Sigmoid(Squasher):
    cpdef double func(self, Vector activations, int k):
        return 1.0 / (1.0 + exp(-activations[k]))
    cpdef double deriv(self, Vector activations, int k):
        return activations[k] * (1.0 - activations[k])

cdef class Softmax(Squasher):
    cpdef double func(self, Vector activations, int k, double eps=0.0):
        cdef double amax = activations.max() # use max(activations) to avoid overflow
        cdef double den = 0.0
        for i from 0 <= i < activations.size:
            den += exp(activations[i] - amax)
            if eps != 0.0 and i == k: den += eps
        return exp(activations[k] - amax + eps) / den
    cpdef double deriv(self, Vector activations, int k):
        return (self.func(activations,k,1e-6) - self.func(activations,k,-1e-6)) / 2e-6

# Loss functions #######################################
# 5.2 PRML Bishop

cdef class Loss:
    cdef Squasher squash
    def __init__(self, squash):
        self.squash = squash()
    cpdef double deriv(self, Vector outputs, Vector targets, int k):
        return 0.0
    cpdef double error(self, Vector outputs, Vector targets):
        return 0.0

cdef class SumOfSquares(Loss):
    def __init__(self, squash=Linear):
        Loss.__init__(self, squash)
    cpdef double deriv(self, Vector outputs, Vector targets, int k):
        return self.squash.deriv(outputs, k) * (targets[k] - outputs[k])
    cpdef double error(self, Vector outputs, Vector targets):
        cdef double err = 0.0
        for k from 0 <= k < outputs.size:
            err += (outputs[k] - targets[k]) * (outputs[k] - targets[k])
        return 0.5 * err

cdef class CrossEntropy(Loss):
    def __init__(self, squash=Sigmoid):
        Loss.__init__(self, squash)
    cpdef double deriv(self, Vector outputs, Vector targets, int k):
        return self.squash.deriv(outputs, k) * (targets[k] - outputs[k])
    cpdef double error(self, Vector outputs, Vector targets):
        cdef double err = 0.0
        for k from 0 <= k < outputs.size:
            err += targets[k]*log(outputs[k]) + (1.0 - targets[k])*log(1.0 - outputs[k])
        return -err

# Matrix operations ##############################################

cdef double dot(Vector vec1, Vector vec2):
    cdef double _sum = 0.0
    for i from 0 <= i < vec1.size:
        _sum += vec1[i] * vec2[i]
    return _sum

cdef double dot_t(Matrix matrix, int j, Vector vec):
    cdef double _sum = 0.0
    for k from 0 <= k < vec.size:
        _sum += matrix.get(k,j) * vec[k]
    return _sum

# Layer class #####################################################

cdef class Layer:
    cdef int n_in
    cdef int n_out
    cdef Vector inputs
    cdef Vector delta_inputs
    cdef Matrix weights
    cdef Vector activations
    cdef Vector outputs
    cdef Vector delta_outputs
    cdef Vector targets
    cdef Loss loss
    cdef int connected
    def __new__(self, int n_in, int n_out, loss=CrossEntropy, squash=None):
        self.n_in = n_in
        self.n_out = n_out
        self.inputs = Vector(n_in, 1.0)
        self.delta_inputs = Vector(n_in, 0.0)
        self.weights = Matrix(n_out, n_in, 1.0)
        self.activations = Vector(n_out, 1.0)
        self.outputs = Vector(n_out, 1.0)
        self.delta_outputs = Vector(n_out, 0.0)
        self.targets = Vector(n_out, 1.0)
        if not squash:
            self.loss = loss()
        else:
            self.loss = loss(squash)
        self.randomize_weights()
        self.connected = 0
    cdef randomize_weights(self):
        for k from 0 <= k < self.n_out:
            for j from 0 <= j < self.n_in:
                self.weights.set(k,j, random.uniform(-2, 2))
    def propagate(self, Vector inputs=None):
        if inputs != None:
            for j from 0 <= j < self.n_in:
                self.inputs[j] = inputs[j]
        self._propagate()
    cdef _propagate(self):
        for k from 0 <= k < self.n_out:
            self.activations[k] = dot(self.weights[k], self.inputs)
        for k from 0 <= k < self.n_out:
            self.outputs[k] = self.loss.squash.func(self.activations, k)
    def backPropagate(self, Vector targets=None):
        if targets != None:
            for k from 0 <= k < self.n_out:
                self.targets[k] = targets[k]
                self.delta_outputs[k] = self.loss.deriv(self.outputs, self.targets, k)
        self._backPropagate()
        if targets != None:
            return self.error()
    cdef _backPropagate(self):
        for j from 0 <= j < self.n_in:
            self.delta_inputs[j] = self.loss.squash.deriv(self.inputs, j) * dot_t(self.weights, j, self.delta_outputs)
    cpdef error(self):
        return self.loss.error(self.outputs, self.targets)
    cpdef updateWeights(self, double learn):
        cdef double momentum = 1.0
        for j from 0 <= j < self.n_in:
            for k from 0 <= k < self.n_out:
                self.weights.set(k,j, self.weights.get(k,j) + (0.5 + (rand() % 100) / 100.0) * learn * (self.delta_outputs[k] * self.inputs[j]))
    cpdef connect(self, Layer next):
        next.connected = 1
        next.inputs = self.outputs
        next.delta_inputs = self.delta_outputs
    cpdef copyWeights(self, Layer other):
        for j from 0 <= j < self.n_in:
            for k from 0 <= k < self.n_out:
                self.weights.set(k,j, other.weights.get(k,j))
    def getInputs(self):
        return self.inputs
    def getWeights(self):
        res = []
        for k from 0 <= k < self.n_out:
            res.append([])
            for j from 0 <= j < self.n_in:
                res[k].append(self.weights.get(k,j))
        return res
    def setWeights(self, weights):
        for k from 0 <= k < self.n_out:
            for j from 0 <= j < self.n_in:
                self.weights.set(k,j, weights[k][j])
    def getOutputs(self, inputs=None):
        if inputs != None:
            self.propagate(inputs)
        return self.outputs
    def dump(self):
        res = dict(inputs  = self.getInputs(),
                   weights = self.getWeights(),
                   outputs = self.getOutputs())
        return {"Layer": res}
    def __repr__(self):
        return "<Layer %d %d>" % (self.n_in, self.n_out)

