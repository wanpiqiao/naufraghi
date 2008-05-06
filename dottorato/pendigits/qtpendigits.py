#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini


import os
import sys

from PyQt4.Qt import *


class PenDigit(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(100, 100)
        self.poly = []
    def sizeHint(self):
        return QSize(100, 100)
    def updatePoly(self, data):
        points = zip(data[0::2], data[1::2])
        print "points:", points
        self.poly = [QPoint(x, 100-y) for (x,y) in points]
        self.update()
    def paintEvent(self, e):
        p = QPainter(self)
        pen = QPen()
        pen.setWidth(2.0)
        p.setRenderHint(QPainter.Antialiasing)
        #p.translate(self.width() / 2, self.height() / 2)
        #side = min(self.width(), self.height())
        #p.scale(side / 100, side / 100)
        lines = zip(self.poly[:-1], self.poly[1:])
        for p1, p2 in lines:
            p.drawLine(p1, p2)

class DatasetViewer(QWidget):
    def __init__(self, data, *args):
        QWidget.__init__(self, *args)
        main = QVBoxLayout(self)
        self.text = QTextEdit(None)
        main.addWidget(self.text)
        self.digit = PenDigit(None)
        main.addWidget(self.digit)
        self.connect(self.text, SIGNAL("cursorPositionChanged()"), self.updateDigit)
        self.text.setPlainText(data.strip())
        self.resize(600, 500)
    def updateDigit(self):
        row = str(self.text.textCursor().block().text()).strip()
        if row:
            row = map(int, row.split(","))[:-1]
            self.digit.updatePoly(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = DatasetViewer(open("pendigits.tra").read())
    todo.show()
    sys.exit(app.exec_())
