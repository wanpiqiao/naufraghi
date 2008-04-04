#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Todo(QWidget):
    def __init__(self, *args):
        super(Todo, self).__init__(*args)

        # Build the view
        vbl = QVBoxLayout(self)
        self.lw = QListWidget(None)
        self.le = QLineEdit(None)
        vbl.addWidget(self.lw)
        vbl.addWidget(self.le)

        # Connect widgets
        QObject.connect(self.le, SIGNAL("editingFinished()"), lambda: self.lw.addItem(self.le.text()))
        QObject.connect(self.le, SIGNAL("editingFinished()"), self.le.clear)

        QObject.connect(self.lw, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.edit) #lambda i: self.le.setText(i.text()))
        #QObject.connect(self.lw, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.lw.removeItemWidget)

    def edit(self, i):
        #self.le.setText(i.text())
        #print i
        #j = self.lw.row(i)
        #print j
        #ii = self.lw.takeItem(j)
        #print ii

        self.le.setText(i.text())
        self.lw.removeItemWidget(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Todo()
    todo.show()
    sys.exit(app.exec_())
