#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import math
import random
from OpenGL.GL import *
from PyQt4.Qt import *
from PyQt4.QtOpenGL import *
from PyQt4 import uic

P1 = [0.0, -1.0, 2.0]
P2 = [1.73, -1.0, -1.0]
P3 = [-1.73, -1.0, -1.0]
P4 = [0.0, 2.0, 0.0]

faces = [(P1, P2, P3), (P1, P3, P4), (P1, P4, P2), (P2, P4, P3)]

class GLWidget(QGLWidget):
    def __init__(self, *args):
        QGLWidget.__init__(self, *args)
        self.xRot = self.yRot = self.zRot = 0
        self.colors = [Qt.yellow, Qt.blue, Qt.green, Qt.red]
        self.setAutoFillBackground(False)
        self.setMinimumSize(200, 200)
        self.setWindowTitle("OpenGL demo")

    def initializeGL(self):
        self.qglClearColor(Qt.black)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        ar = w/float(h)
        glFrustum(-ar, +ar, -1.0, 1.0, 4.0, 45.0)
        glMatrixMode(GL_MODELVIEW)

    def sizeHint(self):
        return QSize(400, 400)

    def paintGL(self):
        self.makeCurrent()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -15.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        for i_f, f in enumerate(faces):
            glBegin(GL_TRIANGLES)
            self.qglColor(self.colors[i_f])
            for p in f:
                glVertex3f(p[0], p[1], p[2])
            glEnd()

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw2D(self):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.white)
        painter.drawText(50, 50, "Hello PyCon 2!")
        painter.end()

    def mousePressEvent(self, event):        self.lastPos = QPoint(event.pos())
    def mouseMoveEvent(self, event):
        dx = 8 * (event.x() - self.lastPos.x())
        dy = 8 * (event.y() - self.lastPos.y())

        if event.buttons() & Qt.LeftButton:
            self.xRot += dy
            self.yRot += dx
        elif event.buttons() & Qt.RightButton:
            self.xRot += dy
            self.zRot += dx

        self.lastPos = QPoint(event.pos())
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = GLWidget()
    todo.show()
    sys.exit(app.exec_())

