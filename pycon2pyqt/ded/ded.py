#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class DDTextEdit(QTextEdit):
    def __init__(self, *args):
        QTextEdit.__init__(self, *args)
        self.setAcceptDrops(True)
        self.setReadOnly(True)

    # Necessario accettare gli eventi di enter drag e move drag
    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        event.acceptProposedAction()

        # L'evento di drop contiene le informazioni a proposito dell'oggetto
        if event.mimeData().hasUrls():
            self.setText('\n'.join([unicode(url.toLocalFile()) for url in event.mimeData().urls()]))

class DedDemo(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.setWindowTitle(self.tr("D&D Demo"))
        
        self.vl = QVBoxLayout(self)
        self.l = QLabel(self.tr("Trascinate qua sotto i vostri file..."))
        self.te = DDTextEdit(None)
        self.vl.addWidget(self.l)
        self.vl.addWidget(self.te)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ded = DedDemo()
    ded.show()
    sys.exit(app.exec_())

