#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2008 Matteo Bertini

import cbplnn as nn

def sigmoid():
    """
    >>> sig = nn.Sigmoid()
    >>> sig.func(0.5)
    0.62245933120185459
    >>> sig.deriv(0.5)
    0.25
    >>> ce = nn.CrossEntropy()
    >>> ce.deriv(2.0, 2.5)
    -1.0
    """

def Layer():
    """
    >>> nn.random.seed(42)
    >>> a = nn.Layer(3, 5)
    >>> b = nn.Layer(5, 1)
    >>> a.connect(b)
    >>> a.propagate([1.0, 1.0, 1.0])
    >>> b.propagate()
    >>> b.backPropagate([0.0])
    0.059802896118833375
    >>> a.backPropagate()
    >>> a.updateWeights(0.05)
    >>> b.updateWeights(0.05)
    >>> a.propagate([1.0, 1.0, 1.0])
    >>> b.propagate()
    >>> b.backPropagate([0.0])
    0.048439615097086802
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
