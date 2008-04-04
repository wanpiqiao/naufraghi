#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Todo(QWidget):
    def __init__(self, *args):
        super(Todo, self).__init__(*args)

        # Build the view
        vbl = QVBoxLayout(self)
        lw = QListWidget(None)
        le = QLineEdit(None)
        vbl.addWidget(lw)
        vbl.addWidget(le)

        # Connect widgets
        QObject.connect(le, SIGNAL("editingFinished()"), lambda: lw.addItem(le.text()))
        QObject.connect(le, SIGNAL("editingFinished()"), le.clear)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Todo()
    todo.show()
    sys.exit(app.exec_())
