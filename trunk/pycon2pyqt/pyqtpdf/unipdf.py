#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class UnicodePDFDemo(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.setWindowTitle(self.tr("Unicode PDF demo"))

        self.vl = QVBoxLayout(self)

        self.l = QLabel(self.trUtf8("Qt (툴킷)"))
        self.te = QTextEdit(None)
        self.pb = QPushButton(self.trUtf8("인쇄!"))
        self.vl.addWidget(self.l)
        self.vl.addWidget(self.te)
        self.vl.addWidget(self.pb)

        QObject.connect(self.pb, SIGNAL("clicked()"), self.doPrint)

    def doPrint(self):
        print self.trUtf8("인쇄!").toUtf8()

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("print...")
        if dialog.exec_() != QDialog.Accepted:
            return

        self.te.print_(printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    updf = UnicodePDFDemo()
    updf.show()
    sys.exit(app.exec_())

