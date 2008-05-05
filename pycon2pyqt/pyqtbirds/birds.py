#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import math
import random
from PyQt4.Qt import *

SIDE = 400.0

class Bird():
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
    def move(self, pos=None):
        if pos:
            self.pos = pos
        else:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
        self.vel[0] += 0.2 * random.uniform(-1,1)
        self.vel[1] += 0.2 * random.uniform(-1,1)
    def dist(self, other):
        return math.sqrt((self.pos[0] - other.pos[0])**2 + (self.pos[1] - other.pos[1])**2)

class Birds(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle(self.tr("Birds"))
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.update)
        self.timer.start(30)
        self.resize(SIDE, SIDE)
        self.birds = [Bird([0,0], [0.1,0.1]) for b in range(100)]
        for i in range(100):
            for bird in self.birds:
                bird.move()
    def paintEvent(self, e):
        p = QPainter(self)
        pen = QPen()
        pen.setWidth(2.0)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)
        side = min(self.width(), self.height())
        p.scale(side / SIDE, side / SIDE)
        #hours, minutes, seconds = time.localtime()[3:-3]
        #p.save()
        #p.rotate(6.0 * seconds)
        #p.drawLine(0,0,100,0)
        #p.restore()
        leaders = self.birds[1:1]
        for bird in self.birds:
            if bird in leaders:
                bird.vel[0] *= 1
                bird.vel[1] *= 1
            else:
                nearest_birds = [i[1] for i in sorted(zip(map(bird.dist, self.birds), self.birds)) if i[0] < 50]
                mean_vel = [sum([b.vel[0] for b in nearest_birds]) / len(nearest_birds),
                            sum([b.vel[1] for b in nearest_birds]) / len(nearest_birds)]
                mean_pos = [sum([b.pos[0] for b in nearest_birds]) / len(nearest_birds),
                            sum([b.pos[1] for b in nearest_birds]) / len(nearest_birds)]
                bird.vel[0] = (mean_vel[0] + bird.vel[0]) / 2.0
                bird.vel[1] = (mean_vel[1] + bird.vel[1]) / 2.0
            bird.move()
            if not -SIDE/2 < bird.pos[0] < SIDE/2:
                bird.pos[0] = bird.pos[0] - cmp(bird.pos[0],0) * SIDE
            if not -SIDE/2 < bird.pos[1] < SIDE/2:
                bird.pos[1] = bird.pos[1] - cmp(bird.pos[1],0) * SIDE
            if bird in leaders:
                pen.setColor(Qt.red)
            else:
                pen.setColor(Qt.black)
            p.setPen(pen)
            p.drawPoint(*bird.pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo = Birds()
    todo.show()
    sys.exit(app.exec_())

