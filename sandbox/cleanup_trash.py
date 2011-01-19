#! /usr/bin/python

import os
import sys
import shutil
import time

MINUTE = 60
HOUR = 60 * MINUTE
DAY  = 24 * HOUR
WEEK =  7 * DAY

MEGA = 1024 * 1024


def getDirSize(dirname):
    res = 0
    for root, _, files in os.walk(dirname):
        ifiles = [os.path.join(root, f) for f in files]
        res += sum([os.path.getsize(f) for f in ifiles if os.path.isfile(f)])
    return res

def getContentsStats(basepath):
    ls = os.listdir
    isdir = os.path.isdir
    def gsize(apath):
        if isdir(apath):
            return getDirSize(apath)
        else:
            return os.path.getsize(apath)
    return [(gsize(i), max(os.stat(i)[-3:]), i) for i in ls(".")]

################################################################################
# Taken from: http://kassiopeia.juls.savba.sk/~garabik/software/pydf/
################################################################################
from math import log
def hfnum(size, base):
    "human readable number"
    if size == 0:
        return "0"
    if size < 0:
        return "?"
    units = ["B", "k", "M", "G", "T", "P", "Z", "Y"]
    power = int(log(size)/log(base))
    if power<0:
        power = 0
    if power>=len(units):
        power = len(units)-1
    nsize = int(round(1.*size/(base**power)))
    if nsize<10 and power>=1:
        power -=1
        nsize = int(round(1.*size/(base**power)))
    r = str(nsize)+units[power]
    return r
################################################################################

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-r", "--rtime", dest="rtime", default=2, type="int",
                      help="Oldness hint in weeks, default = %default")
    parser.add_option("-m", "--msize", dest="msize", default=10, type="int",
                      help="Bigness hint in Mb, default = %default")
    parser.add_option("-d", "--delete",
                      action="store_true", dest="delete", default=False,
                      help="Delete old/big files, default = %default")
    (options, args) = parser.parse_args()

    if not args:
        os.chdir(os.path.expanduser("~/.Trash"))
    else:
        os.chdir(args[0])
    stats = getContentsStats(".")
    trash_list = sorted([(size * mtime, name, size) for size, mtime, name in stats], reverse=True)
    border_value = options.msize * MEGA * (time.time() - options.rtime * WEEK)
    remove_list = [(name, size) for v, name, size in trash_list if v > border_value]
    print "#"*40
    print "# rtime = %d Weeks" % options.rtime
    print "# msize = %d Mb" % options.msize
    print "#"*40
    todel_size = 0
    if options.delete:
        print "!! DELETE MODE !! Waiting 5 seconds..."
        print "[",
        for i in range(10):
            sys.stdout.write("%d" % (i + 1))
            sys.stdout.write(" . ")
            sys.stdout.flush()
            time.sleep(0.5)
        print "]"
    for name, size in remove_list:
        todel_size += size
        if options.delete:
            print "REMOVING...",
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)
        print "[%4s %4s] %s" % ({True: "DIR", False: "FILE"}[os.path.isdir(name)], hfnum(size, 1024), name)
    print "#"*40
    print "# TOTAL size:", hfnum(todel_size, 1024)
    print "#"*40
        
