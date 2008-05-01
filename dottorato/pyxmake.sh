#!/bin/bash

cython cbplnn.pyx && python setup.py build_ext --inplace && python test_cbplnn.py
