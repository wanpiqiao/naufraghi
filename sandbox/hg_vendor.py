#!/usr/bin/python

import os.path
import urllib
import re
import tarfile
import subprocess

pyqt_base_uri = "http://www.riverbankcomputing.com/Downloads/Snapshots/PyQt4/"

def log(*args):
    print " ".join(args)

def download(pyqt_base_uri, pyqt_gz):
    if not os.path.isfile(pyqt_gz):
        log("Downloading ...")
        pyqt_snap_uri = os.path.join(pyqt_base_uri, pyqt_gz)
        urllib.urlretrieve(pyqt_snap_uri, pyqt_gz)
        log("Done downloading!")
        return True
    else:
        log("Last version already downloaded!")
        return False

if __name__ == "__main__":
    pyqt_snap_index = urllib.urlopen(pyqt_base_uri).read()
    pyqt_gz, pyqt_ver = re.search("(PyQt-x11-gpl-4-(snapshot-[0-9]+).tar.gz)", pyqt_snap_index).groups()
    log("Found PyQt version", pyqt_ver, "online")
    download(pyqt_base_uri, pyqt_gz)

