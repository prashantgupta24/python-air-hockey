import math
from random import randint

import pyxel

class App:
    def __init__(self):
        print("Starting game...")
        pyxel.init(256, 256)
        self.border = 15

        #paddle dimensions
        self.pLength = 20
        self.pMovingDistance = 5 #pixels to move paddle on key press

        #paddle co-ordinates
        self.p1x = self.border
        self.p1y = pyxel.height / 2

        self.p2x = pyxel.width - self.border
        self.p2y = pyxel.height / 2

        #ball attributes
        self.cx = pyxel.width / 2
        self.cy = pyxel.height / 2
        self.cr = 5
        # self.cm = 1
        # self.cc = 50
        # self.cxMovingLength = randint(-10,10)
        # self.cyMovingLength = randint(-10,10)
        self.vx = 1
        self.vy = 2

        pyxel.run(self.update, self.draw)

    #def distanceOfBallFromPoint()

    def checkBallCollision(self):

        hasBallCollided = False

        topPointY = self.cy - self.cr

        bottomPointY = self.cy + self.cr

        leftPointX = self.cx - self.cr

        rightPointX = self.cx + self.cr

        #print(topPointY)
        #top or down
        if topPointY <= self.border or bottomPointY >= pyxel.height - self.border:
        #if topPointY <= self.border:
            hasBallCollided = True
            self.vy = self.vy * -1
            print("collided!")

        elif leftPointX <= self.p1x or rightPointX >= pyxel.width - self.border:
            hasBallCollided = True
            self.vx = self.vx * -1
            print("collided!")

        #return hasBallCollided
        #paddle
        #if distanceOfBallFromPoint()

    def update(self):
        #print("update")
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_W):
            if self.p1y > self.border:
                self.p1y = (self.p1y - self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_S):
            if self.p1y + self.pLength + self.pMovingDistance < pyxel.height-self.border:
                self.p1y = (self.p1y + self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_UP):
            if self.p2y > self.border:
                self.p2y = (self.p2y - self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_DOWN):
            if self.p2y + + self.pLength + self.pMovingDistance < pyxel.height-self.border:
                self.p2y = (self.p2y + self.pMovingDistance)

        self.checkBallCollision()
        # if self.checkBallCollision():
        #     self.cMovingLength = self.cMovingLength * -1
            # self.cc = self.cy - self.cm * self.cx

        # if not self.checkBallCollision():
        #     self.cx = self.cx + self.cMovingLength
        #     self.cy = self.cm * self.cx + self.cc
        #     print(self.cMovingLength)
        # else:
        #     self.cMovingLength = self.cMovingLength * -1
        #     self.cx = self.cx + self.cMovingLength
        #     self.cy = self.cm * self.cx + self.cc
        #     print(self.cMovingLength)
        self.cx = self.cx + self.vx
        self.cy = self.cy + self.vy

        print(f'x is {self.cx} and y is {self.cy}')

    def draw(self):
        #print("draw")
        pyxel.cls(0)

        pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
        pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)

        pyxel.circ(self.cx, self.cy, self.cr, 7)

App()
