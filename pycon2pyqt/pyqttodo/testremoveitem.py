#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

app = QApplication(sys.argv)

lw = QListWidget(None)
lw.addItem("test1")
lw.addItem("test2")
assert lw.count() == 2

i = lw.row(lw.item(0))
lw.takeItem(i)
assert lw.count() == 1

lw.removeItemWidget(lw.item(0))
assert lw.count() == 0, lw.count()
