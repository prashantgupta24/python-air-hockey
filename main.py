import random

import pyxel

class App:
    def __init__(self):
        print("Starting game...")
        pyxel.init(256, 256, caption="Air hockey", scale=8, fps=22)
        self.initValues()
        #Scores are per game, not per round
        self.p1Score = 0
        self.p2Score = 0
        pyxel.run(self.update, self.draw)

    def initValues(self):

        #screen setup
        self.border = 20 #anything less than 20 doesn't work

        #paddle attributes
        self.pLength = 30
        self.pMovingDistance = 8 #pixels to move paddle on key press

        #game attributes
        self.endGameScore = 2
        self.hasGameEnded = False
        self.isRoundActive = True
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
        self.cr = 7

        #ball moving parameters
        self.vx = random.choice([random.uniform(2, 3), random.uniform(-3, -2)])
        self.vy = random.choice([random.uniform(2, 3), random.uniform(-3, -2)])
        # self.vx = -2.5
        # self.vy = -3

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
                            print("hit top edge of paddle 1 with difference : ", self.p1y - self.cy)
                            self.vx = self.vx * -1
                            self.vy = self.vy * -1
                            self.vx = self.vx - (self.p1y-self.cy)/10
                        else:
                            print("hit bottom edge of paddle 1 with difference : ", self.cy - self.p1y)
                            self.vx = self.vx * -1
                            self.vx = self.vx - (self.cy-self.p1y)/10
                    else:
                        print("ball coming from bottom")
                        # hitting top edge
                        if self.cy < self.p1y:
                            print("hit top edge of paddle 1!")
                            self.vx = self.vx * -1
                            self.vx = self.vx - (self.p1y-self.cy)/10
                        else:
                            print("hit bottom edge of paddle 1!")
                            self.vx = self.vx * -1
                            self.vy = self.vy * -1
                            self.vx = self.vx - (self.cy-self.p1y)/10
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


    def checkGameEndScore(self):
        if self.p1Score == self.endGameScore or self.p2Score == self.endGameScore:
            self.hasGameEnded = True

    def checkBallCollision(self):

        topPointY = self.cy - self.cr
        bottomPointY = self.cy + self.cr

        leftPointX = self.cx - self.cr
        rightPointX = self.cx + self.cr

        #top or down
        if topPointY < 1 or bottomPointY > pyxel.height - 1:
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
        if self.cx > self.p2x:
            print("missed by p2!")
            self.p1Score += 1
            self.isRoundActive = False
        elif self.cx < self.p1x:
            print("missed by p1!")
            self.p2Score += 1
            self.isRoundActive = False


    def updateControlKeys(self):
        if pyxel.btn(pyxel.KEY_W):
            if self.p1y > 1:
                self.p1y = (self.p1y - self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_S):
            if self.p1y + self.pLength + self.pMovingDistance < pyxel.height-1:
                self.p1y = (self.p1y + self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_UP):
            if self.p2y > 1:
                self.p2y = (self.p2y - self.pMovingDistance)

        if pyxel.btn(pyxel.KEY_DOWN):
            if self.p2y + + self.pLength + self.pMovingDistance < pyxel.height-1:
                self.p2y = (self.p2y + self.pMovingDistance)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if not self.isRoundActive:
            if pyxel.btnp(pyxel.KEY_ENTER):
                if self.hasGameEnded:
                    self.p1Score = 0
                    self.p2Score = 0
                self.initValues()


        if self.isRoundActive:
            self.updateControlKeys()

            self.checkBallCollision()
            self.checkGameEndScore()

            self.cx = self.cx + self.vx
            self.cy = self.cy + self.vy

            #print(f'x is {self.cx} and y is {self.cy}')


    def draw(self):

        pyxel.cls(0)

        pyxel.line(pyxel.width/2, 1, pyxel.width/2, pyxel.height, 1)
        # draw score
        s = f'SCORE {self.p1Score}'
        pyxel.text(self.border, 4, s, 1)
        pyxel.text(self.border, 4, s, 7)

        s = f'SCORE {self.p2Score}'
        pyxel.text(pyxel.width - self.border*2, 4, s, 1)
        pyxel.text(pyxel.width - self.border*2, 4, s, 7)

        if self.isRoundActive:
            pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
            pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)
            pyxel.circ(self.cx, self.cy, self.cr, 7)

        else:
            pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
            pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)

        if self.hasGameEnded:
            s = f'You Won!!!'

            if self.p1Score > self.p2Score:
                pyxel.text(self.border, 20, s, 1)
                pyxel.text(self.border, 20, s, 7)
            else:
                pyxel.text(pyxel.width - self.border*2, 20, s, 1)
                pyxel.text(pyxel.width - self.border*2, 20, s, 7)

            pyxel.text(1, pyxel.width - self.border, "GAME OVER. Press Enter to restart", 2)
App()
