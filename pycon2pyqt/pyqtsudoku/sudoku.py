#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from PyQt4.Qt import *

class Number(QLabel):
    def __init__(self, *args):
        super(Number, self).__init__(*args)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    def sizeHint(self):
        return QSize(40, 40)

class Grid(QGridLayout):
    def __init__(self, *args):
        super(Grid, self).__init__(*args)
        self.setSpacing(0)
    def heightForWidth(self, w):
        return w
    def hasHeightForWidth(self):
        return True

class Sudoku(QWidget):
    def __init__(self, *args):
        super(Sudoku, self).__init__(*args)
        self.setWindowTitle(self.tr("Sudoku"))

        # Build the view
        self.grid = Grid(self)
        self.setStyleSheet("Number {border: 1px solid grey;}")
        
        for i in range(9):
            for j in range(9):
                ss = ""
                l = Number("%s,%s" % (i,j))
                if j and j % 3 == 0:
                    ss += "border-left: 2px solid black;"                    
                if i and i % 3 == 0:
                    ss += "border-top: 2px solid black;"
                l.setStyleSheet(ss)
                self.grid.addWidget(l, i, j)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Sudoku()
    todo.show()
    sys.exit(app.exec_())
