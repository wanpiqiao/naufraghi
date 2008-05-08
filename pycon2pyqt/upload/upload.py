#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import time
import math
import random
from ftplib import FTP

from PyQt4.Qt import *
from PyQt4 import uic

class Dropper(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.setAcceptDrops(True)
        self.setText("Drop files here")
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
            filepath = [unicode(url.toLocalFile()) for url in event.mimeData().urls()][0]
            self.setText(filepath)
            self.emit(SIGNAL("upload"), filepath)

class UploadConfig(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        uic.loadUi("upload.ui", self)
    def getConfig(self):
        user, ftp = str(self.ledit_ftp.text()).rsplit("@", 1)
        http = str(self.ledit_http.text())
        pwd = str(self.ledit_pwd.text())
        return locals()

class Uploader(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.main = QVBoxLayout(self)
        self.dropper = Dropper(None)
        self.config = UploadConfig(None)
        self.main.addWidget(self.dropper)
        self.main.addWidget(self.config)
        self.connect(self.dropper, SIGNAL("upload"), self.upload)
	
    def upload(self, filepath):
        config = self.config.getConfig()
        ftp = FTP(config["ftp"], config["user"], config["pwd"])
        self.dropper.setText("Uploading '%s'..." % filepath)
        ftp.storbinary('STOR '+os.path.basename(filepath), open(filepath))
        
        uri = os.path.join(config["http"], os.path.basename(filepath))
        self.dropper.setText(uri)
        qApp.clipboard().setText(uri)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Uploader()
    todo.show()
    sys.exit(app.exec_())
