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
    samples = gen_samples(n=10, d=2, k=3)
    print ", ".join(["feat%d" % f for f in range(len(samples[0][0]))] + ["couple"])
    for i, row in enumerate(samples):
        for j, samp in enumerate(row):
            for k, v in enumerate(samp):
                print ", ".join(map(str, list(v))) + ", couple%d-%d" % (i, j)
