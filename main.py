from random import randint

import pyxel

class App:
    def __init__(self):
        print("Starting game...")
        pyxel.init(256, 256)
        self.initValues()
        pyxel.run(self.update, self.draw)

    def initValues(self):

        #screen setup
        self.border = 15

        #paddle attributes
        self.pLength = 30
        self.pMovingDistance = 8 #pixels to move paddle on key press

        #game attributes
        self.isGameActive = True
        self.hitCount = 0
        self.increaseSpeedAfter = 3
        self.increaseSpeedFactor = 1.2

        #paddle co-ordinates
        self.p1x = self.border
        self.p1y = pyxel.height / 2

        self.p2x = pyxel.width - self.border
        self.p2y = pyxel.height / 2

        #ball attributes
        self.cx = pyxel.width / 2
        self.cy = pyxel.height / 2
        self.cr = 8

        #ball moving parameters
        # self.vx = randint(-2,-1)
        # self.vy = randint(-2,-1)
        self.vx = -2.5
        self.vy = -3

    def properHit(self, paddleY):
        if paddleY <= self.cy <= paddleY + self.pLength :
            return True

        return False

    def handlePaddle1(self, leftPointX, topPointY, bottomPointY):

        hasBallCollided = False

        #entering the realm of p1
        if leftPointX <= self.p1x and self.vx < 0:
            if bottomPointY < self.p1y or topPointY > self.p1y + self.pLength:
                pass
            else:
                print("collided with left paddle!")
                hasBallCollided = True
                print(f'x is {self.cx} and y is {self.cy}')
                #determine angle of hit if not proper hit
                if not self.properHit(self.p1y):
                    if self.vy > 0:
                        print("ball coming from top!")
                        # hitting top edge
                        if self.cy < self.p1y:
                            print("hit top edge of paddle 1!")
                            self.vx = self.vx * -1
                            self.vy = self.vy * -1
                            self.vx = self.vx - 0.1
                        else:
                            print("hit bottom edge of paddle 1!")
                            self.vx = self.vx * -1
                    else:
                        print("ball coming from bottom")
                        # hitting top edge
                        if self.cy < self.p1y:
                            print("hit top edge of paddle 1!")
                            self.vx = self.vx * -1
                            self.vx = self.vx - 0.1
                        else:
                            print("hit bottom edge of paddle 1!")
                            self.vx = self.vx * -1
                            self.vy = self.vy * -1
                            self.vx = self.vx - 0.1
                else:
                    print("proper hit!")
                    self.vx = self.vx * -1

        return hasBallCollided


    def handlePaddle2(self, rightPointX, topPointY, bottomPointY):

        hasBallCollided = False

        #entering the realm of p2
        if rightPointX >= self.p2x and self.vx > 0:
            # if bottomPointY < self.p2y or topPointY > self.p2y + self.pLength:
            #     pass
            # else:
            #     #determine angle of hit
            #     self.vx = randint(1,3)
            #     self.vy = randint(1,3)
            print("collided with right paddle!")
            hasBallCollided = True
            #print(f'hit count is {self.hitCount}')

            self.vx = self.vx * -1

        return hasBallCollided


    def checkBallCollision(self):

        topPointY = self.cy - self.cr
        bottomPointY = self.cy + self.cr

        leftPointX = self.cx - self.cr
        rightPointX = self.cx + self.cr

        #top or down
        if topPointY < self.border or bottomPointY > pyxel.height - self.border:
            self.vy = self.vy * -1
            #print("collided top/bottom!")

        ballHitP1 = self.handlePaddle1(leftPointX=leftPointX, topPointY=topPointY, bottomPointY=bottomPointY)
        ballHitP2 = self.handlePaddle2(rightPointX=rightPointX, topPointY=topPointY, bottomPointY=bottomPointY)

        if ballHitP1 or ballHitP2:
            self.hitCount += 1
            if self.hitCount > 1 and self.hitCount % self.increaseSpeedAfter == 0:
                print(f'Increasing speed after {self.hitCount} hits')
                self.vx = self.vx * self.increaseSpeedFactor
                self.vy = self.vy * self.increaseSpeedFactor

        #missed both
        if self.cx > self.p2x or self.cx < self.p1x:
            print("missed!")
            self.isGameActive = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
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

            #print(f'x is {self.cx} and y is {self.cy}')


    def draw(self):

        if self.isGameActive:

            pyxel.cls(0)

            pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
            pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)

            pyxel.circ(self.cx, self.cy, self.cr, 7)

        else:
            pyxel.cls(0)

            pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
            pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)
App()
