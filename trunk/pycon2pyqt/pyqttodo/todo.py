#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Todo(QWidget):
    def __init__(self, *args):
        super(Todo, self).__init__(*args)
        self.setWindowTitle(self.tr("PyConDue"))
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "PyConDue", "ToDo", self)

        # Build the view
        vbl = QVBoxLayout(self)
        self.lw = QListWidget(None)
        self.le = QLineEdit(None)
        vbl.addWidget(self.lw)
        vbl.addWidget(self.le)

        # Fill the view
        for todo in self.settings.allKeys():
            self.lw.addItem(self.settings.value(todo).toString())

        # Connect widgets
        QObject.connect(self.le, SIGNAL("returnPressed()"), lambda: self.lw.addItem(self.le.text()))
        QObject.connect(self.le, SIGNAL("returnPressed()"), self.le.clear)

        QObject.connect(self.lw, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.edit)

    def edit(self, i):
        self.lw.takeItem(self.lw.row(i))
        self.lw.setCurrentItem(None)

        self.le.setText(i.text())
        self.le.selectAll()
        self.le.setFocus()

    def closeEvent(self, event):
        for i in xrange(self.lw.count()):
            self.settings.setValue(u"todo/%d" % (i,), QVariant(self.lw.item(i).text()))
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Todo()
    todo.show()
    sys.exit(app.exec_())
