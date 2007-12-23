#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Search and replace utility
------------------------------------------
Usage:
    sar.py searchre replacere [globfilter]
Output:
    a patch -p0 < patch.diff
"""

import sys
import os
import os.path
import glob
import re
import difflib

pjoin = os.path.join

def list_recursive_files(basepath, glob_filter):
    for filename in glob.glob(pjoin(basepath, glob_filter)):
        if os.path.isfile(filename):
            yield filename
    for root, dirs, files in os.walk(basepath):
        for dir in dirs:
            for filename in glob.glob(pjoin(pjoin(root, dir), glob_filter)):
                if os.path.isfile(filename):
                    yield filename


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print "Provide: searchre replacere [globfilter]"
        sys.exit(0)

    if len(args) < 3:
        args.append("*")

    if len(args) != 3:
        print "Invalig args!", args
        sys.exit(0)

    searchre, replacere, glob_filter = args

    for filename in list_recursive_files(os.getcwd(), glob_filter):
        sys.stderr.write("Processing file %s... " % filename)
        res = orig = open(filename).read()
        res = re.sub(searchre, replacere, res)

        if orig != res:
            sys.stderr.write("MATCH FOUND")
            print "Index:", filename
            print "=" * 80
            print ''.join(list(difflib.unified_diff(orig.splitlines(1),
                                                    res.splitlines(1),
                                                    filename + " (original)",
                                                    filename + " (modified)"))),
        sys.stderr.write("\n")
