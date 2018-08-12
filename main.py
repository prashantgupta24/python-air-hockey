import math
from random import randint

import pyxel

class App:
    def __init__(self):
        print("Starting game...")
        pyxel.init(256, 256)
        self.border = 15

        self.initValues()
        #paddle dimensions
        self.pLength = 20
        self.pMovingDistance = 5 #pixels to move paddle on key press

        pyxel.run(self.update, self.draw)

    #def distanceOfBallFromPoint()

    def initValues(self):

        self.isGameActive = True
        #paddle co-ordinates
        self.p1x = self.border
        self.p1y = pyxel.height / 2

        self.p2x = pyxel.width - self.border
        self.p2y = pyxel.height / 2

        #ball attributes
        self.cx = pyxel.width / 2
        self.cy = pyxel.height / 2
        self.cr = 5

        #ball moving parameters
        # self.vx = randint(-2,-1)
        # self.vy = randint(-2,-1)
        self.vx = 1
        self.vy = 2

    def checkBallCollision(self):

        hasBallCollided = False

        topPointY = self.cy - self.cr
        bottomPointY = self.cy + self.cr

        leftPointX = self.cx - self.cr
        rightPointX = self.cx + self.cr

        #top or down
        if topPointY < self.border or bottomPointY > pyxel.height - self.border:
            hasBallCollided = True
            self.vy = self.vy * -1
            print("collided top/bottom!")

        #entering the realm of p1
        if leftPointX <= self.p1x and self.vx < 0:
            if bottomPointY < self.p1y or topPointY > self.p1y + self.pLength:
                pass
            else:
                #determine angle of hit
                print("collided with left paddle!")
                self.vx = self.vx * -1

        #entering the realm of p2
        if rightPointX >= self.p2x and self.vx > 0:
            if bottomPointY < self.p2y or topPointY > self.p2y + self.pLength:
                pass
            else:
                #determine angle of hit
                print("collided with right paddle!")
                self.vx = self.vx * -1

        #missed both
        if self.p2x < self.cx < self.p1x:
            print("missed!")
            self.isGameActive = False


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_H):
            self.initValues()

        if self.isGameActive:
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

            self.cx = self.cx + self.vx
            self.cy = self.cy + self.vy

            print(f'x is {self.cx} and y is {self.cy}')

    def draw(self):

        if self.isGameActive:

            pyxel.cls(0)

            pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
            pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)

            pyxel.circ(self.cx, self.cy, self.cr, 7)

App()
