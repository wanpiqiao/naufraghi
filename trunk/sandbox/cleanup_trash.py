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
        res += sum([os.path.getsize(os.path.join(root, f)) for f in files if os.path.isfile(f)])
    print dirname, res
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

    os.chdir(os.path.expanduser("~/.Trash"))
    stats = getContentsStats(".")
    trash_list = sorted([(size * mtime, name) for size, mtime, name in stats], reverse=True)
    border_value = options.msize * MEGA * (time.time() - options.rtime * WEEK)
    remove_list = [name for v, name in trash_list if v > border_value]
    print "#"*40
    print "# rtime = %d Weeks" % options.rtime
    print "# msize = %d Mb" % options.msize
    print "#"*40
    for name in remove_list:
        print os.path.isdir(name) and "[ DIR]" or "[FILE]",
        if options.delete:
            print "REMOVING...",
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)
        print name
        
