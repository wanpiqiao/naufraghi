#! /usr/bin/python

import os
import sys
import shutil
import time

MINUTE = 60
HOUR = 60 * MINUTE
DAY  = 24 * HOUR
WEEK =  7 * DAY

rtime = 2 * WEEK

MEGA = 1024 * 1024

msize = 10 * MEGA


def getDirSize(dirname):
    res = 0
    for root, _, files in os.walk(dirname):
        res += sum([os.path.getsize(os.path.join(root, f)) for f in files if os.path.isfile(f)])
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

if __name__ == "__main__":
    #os.chdir("/Users/matteo/.Trash/")
    stats = getContentsStats(".")
    trash_list = sorted([(size * mtime, name) for size, mtime, name in stats], reverse=True)
    border_value = msize * (time.time() - rtime)
    remove_list = [name for v, name in trash_list if v > border_value]
    print "#"*40
    print "# rtime = %d Weeks" % (rtime / WEEK)
    print "# msize = %d Mb" % (msize / MEGA)
    print "#"*40
    for name in remove_list:
        print os.path.isdir(name) and "[ DIR]" or "[FILE]",
        if "--delete" in sys.argv:
            print "REMOVING...",
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)
        print name
        
