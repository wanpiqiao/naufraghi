#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright (c) 2007, Giovanni Bajo
# Copyright (c) 2008, Matteo Bertini

import sys
import os
from os.path import *
from subprocess import *
import shutil


def get_tracked(wcdir):
    """
    Return tracked files in wcdir.
    If the dir is not versioned, returns all files.
    """
    wcdir = abspath(wcdir)
    if ".svn" in os.listdir(wcdir):
        svn_ls = Popen(["svn", "ls", "-R", wcdir], stdout=PIPE).stdout.read()
        return [normpath(l) for l in svn_ls.splitlines()]
    else:
        allfiles = []
        for root, dirs, files in os.walk(wcdir):
            allfiles += [normpath(join(root, p)[len(wcdir)+1:]) for p in files+dirs]
        return allfiles

def vendor_upgrade_svn(src, dst):
    """
    Copy all tracked file/dir from src to dst
    Remove and Add changes
    """
    print "Analyzing %s..." % src
    src_tracked = set(get_tracked(src))
    print "Analyzing %s..." % dst
    dst_tracked = set(get_tracked(dst))

    modified = src_tracked & dst_tracked
    added = src_tracked - dst_tracked
    removed = dst_tracked - src_tracked
    print "%d Modified, %d Added, %d Removed" % (len(modified), len(added), len(removed))

    print "Differences:"
    for tracked in sorted(modified):
        if isdir(join(src, tracked)):
            # This represents a property's change. We don't track properties
            # (like svn export does too).
            print "M [DIR ] %s" % tracked
        else:
            print "M [FILE] %s" % tracked
            shutil.copy2(join(src, tracked), join(dst, tracked))

    for tracked in sorted(added):
        if isdir(join(src, tracked)):
            print "A [DIR ] %s" % tracked
            os.mkdir(join(dst, tracked))
        else:
            print "A [FILE] %s" % tracked
            shutil.copy2(join(src, tracked), join(dst, tracked))
        call(["svn", "add", "--depth", "empty", join(dst, tracked)])

    for tracked in sorted(removed, reverse=True):
        if isdir(join(dst, tracked)):
            print "D [DIR ] %s" % tracked
        else:
            print "D [FILE] %s" % tracked
        call(["svn", "rm", join(dst, tracked)])
    print "\nDone!\n\n"


if __name__ == "__main__":
    print "Vendor branch management tool (svn version)"
    if len(sys.argv) > 2:
        src = abspath(sys.argv[1])
        dst = abspath(sys.argv[2])
        if not isdir(src):
            print "\nFolder '%s' missing!" % src
        elif not isdir(dst):
            print "\nFolder '%s' missing!" % dst
        else:
            vendor_upgrade_svn(src, dst)
    else:
        print "\nUsage:"
        print "  %s srcdir svndir" % sys.argv[0]
