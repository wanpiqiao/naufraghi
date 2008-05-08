#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Todo(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle(self.tr("PyConDue"))
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "PyConDue", "ToDo", self)

        # Build the view
        vbl = QVBoxLayout(self)
        self.lv = QListView(None)
        self.lm = QStringListModel(None)
        self.lv.setModel(self.lm)
        self.le = QLineEdit(None)
        vbl.addWidget(self.lv)
        vbl.addWidget(self.le)

        # Fill the view        
        self.lm.setStringList([self.settings.value(todo).toString() for todo in self.settings.allKeys()])

        # Connect widgets
        QObject.connect(self.le, SIGNAL("returnPressed()"), self.insert)
        QObject.connect(self.le, SIGNAL("returnPressed()"), self.le.clear)

        QObject.connect(self.lv, SIGNAL("doubleClicked(const QModelIndex &)"), self.edit)

    def insert(self):
        self.lm.insertRows(0, 1)
        self.lm.setData(self.lm.index(0), QVariant(self.le.text()), Qt.DisplayRole)

    def edit(self, mi):
        self.le.setText(self.lm.data(mi, Qt.DisplayRole).toString())

        self.lm.removeRows(mi.row(), 1)
        self.lv.clearSelection()

        self.le.selectAll()
        self.le.setFocus()

    def closeEvent(self, event):
        self.settings.clear()
        for i, item in enumerate(self.lm.stringList()):
            self.settings.setValue(u"todo/%d" % (i,), QVariant(item))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #translator = QTranslator()
    #translator.load("todo-en.qm")
    #app.installTranslator(translator)
    todo = Todo()
    todo.show()
    sys.exit(app.exec_())

