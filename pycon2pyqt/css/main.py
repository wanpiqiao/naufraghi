#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import math
import random
from PyQt4.Qt import *
from PyQt4 import uic

class SimpleForm(QDialog):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        uic.loadUi("simpleform.ui", self)
        self.lineEdit.setText("Foobar")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = SimpleForm()
    todo.show()
    sys.exit(app.exec_())
