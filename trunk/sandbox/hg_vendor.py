#!/usr/bin/python

import os.path
import urllib
import re

pyqt_base_uri = "http://www.riverbankcomputing.com/Downloads/Snapshots/PyQt4/"

if __name__ == "__main__":
    pyqt_snap_index = urllib..urlopen(pyqt_base_uri).read()
    pyqt_gz, pyqt_ver = re.search("(PyQt-x11-gpl-4-(snapshot-[0-9]+).tar.gz)", pyqt_snap_index).groups()
    pyqt_snap_uri = os.path.join(pyqt_base_uri, pyqt_gz)

