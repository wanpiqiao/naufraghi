#!/usr/bin/python
# -*- encoding: utf-8 -*-

from pylab import *
from numpy import random

def gen_samples(n=100, d=5, k=3):
    samples = []
    random.seed(0)
    for _ in range(n):
        sample = [randn(d)]
        for _ in range(k-1):
            sample.append(sample[-1] + randn(d) * 0.05)
        couple = [v + randn(d) * 0.05 for v in sample]
        samples.append(zip(sample, couple))
    return samples


if __name__ == "__main__":
    print "block, couple, sample"
    for i, row in enumerate(gen_samples(n=10, d=2, k=3)):
        for j, samp in enumerate(row):
            for k, v in enumerate(samp):
                print ", ".join(map(str, [i, j] + list(v)))
