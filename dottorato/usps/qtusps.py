#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini


import os
import sys
import gzip

from PyQt4.Qt import *

os.chdir(os.path.abspath(os.path.dirname(__file__)))

class USPS(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(100, 100)
        self.image = QImage(16, 16, QImage.Format_RGB32)
    def sizeHint(self):
        return QSize(100, 100)
    def updatePoly(self, data):
        picture = [data[16*i:16*(i+1)] for i in range(16)]
        print "picture:", len(picture), len(picture[0])
        for y, row in enumerate(picture):
            for x, pixel in enumerate(row):
                gray = [255 - int((1 + pixel) * 127)]*3 # pixel is [0, 2]
                print "%3d" % gray[0],
                self.image.setPixel(x, y, qRgb(*gray))
            print
        self.update()
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        #p.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        p.scale(side / 16, side / 16)
        p.drawImage(self.image.rect(), self.image, self.rect())



class DatasetViewer(QWidget):
    def __init__(self, data, *args):
        QWidget.__init__(self, *args)
        main = QVBoxLayout(self)
        self.text = QTextEdit(None)
        self.text.setLineWrapMode(QTextEdit.NoWrap)
        main.addWidget(self.text)
        self.digit = USPS(None)
        main.addWidget(self.digit)
        self.connect(self.text, SIGNAL("cursorPositionChanged()"), self.updateDigit)
        self.text.setPlainText(data.strip())
        self.resize(600, 500)
    def updateDigit(self):
        row = str(self.text.textCursor().block().text()).strip()
        if row:
            row = map(float, row.split(" "))[1:]
            self.digit.updatePoly(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = "".join(gzip.open("zip.train.gz").readlines()[:100])
    todo = DatasetViewer(data)
    todo.show()
    sys.exit(app.exec_())
