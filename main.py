import random
import logging
import pyxel

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)

class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.info("Starting game...")

        pyxel.init(256, 256, caption="Air hockey", scale=8, fps=40)
        self.initValues()
        self.initSound()

        # Scores are per game, not per round
        self.p1Score = 0
        self.p2Score = 0

        self.p1KeyUp = pyxel.KEY_W
        self.p1KeyDown = pyxel.KEY_S
        self.p2KeyUp = pyxel.KEY_UP
        self.p2KeyDown = pyxel.KEY_DOWN

        pyxel.run(self.update, self.draw)

    def initValues(self):

        # screen setup
        self.border = 20  # anything less than 20 doesn't work

        # paddle attributes
        self.pLength = 30
        self.pMovingDistance = 8  # pixels to move paddle on key press

        # game attributes
        self.endGameScore = 3
        self.hasGameEnded = False
        self.isRoundActive = True
        self.hitCount = 0
        self.increaseSpeedAfter = 3
        self.increaseSpeedFactor = 1.2

        # paddle co-ordinates
        self.p1x = self.border
        self.p1y = pyxel.height / 2

        self.p2x = pyxel.width - self.border
        self.p2y = pyxel.height / 2

        # ball attributes
        self.Bx = pyxel.width / 2
        self.By = pyxel.height / 2
        self.Br = 7

        # ball coordinates dict (will update on each frame)
        self.BCoordinates = {}

        # ball moving parameters
        self.vx = random.choice([random.uniform(1, 2), random.uniform(-2, -1)])
        self.vy = random.choice([random.uniform(1, 2), random.uniform(-2, -1)])

    def initSound(self):
        pyxel.sound(0).set('g1a#1d#2b2', 's', '7654', 's', 1)

        a = 'g1c2d2e2 e2e2f2f2'
        b = 'e2e2e2c2 c2c2c2c2'
        c = 'g2g2g2d2 d2d2d2d2'

        pyxel.sound(1).set('a3d#3a#2f#2d2b1g1d#1', 's', '77654321', 's', 10)
        pyxel.sound(2).set(a + b + a + c, 's', '4', 'nnnn vvnn vvff nvvf', 30)

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

            self.Bx = self.Bx + self.vx
            self.By = self.By + self.vy

            #self.logger.debug(f'ball position: x is {self.Bx} and y is {self.By}')

    def draw(self):

        pyxel.cls(0)

        pyxel.line(pyxel.width / 2, 1, pyxel.width / 2, pyxel.height, 1)

        pyxel.line(self.p1x, self.p1y, self.p1x, self.p1y + self.pLength, 7)
        pyxel.line(self.p2x, self.p2y, self.p2x, self.p2y + self.pLength, 7)

        # draw p1 score
        s = f'SCORE {self.p1Score}'
        pyxel.text(self.border, 4, s, 1)
        pyxel.text(self.border, 4, s, 7)

        # draw p2 score
        s = f'SCORE {self.p2Score}'
        pyxel.text(pyxel.width - self.border * 2, 4, s, 1)
        pyxel.text(pyxel.width - self.border * 2, 4, s, 7)

        if self.isRoundActive:
            pyxel.circ(self.Bx, self.By, self.Br, 7)

        else:
            pyxel.text(1, pyxel.width - self.border,
                       "Press Enter to continue", 2)

        if self.hasGameEnded:
            s = f'You Won!!!'

            if self.p1Score > self.p2Score:
                pyxel.text(self.border, 20, s, 1)
                pyxel.text(self.border, 20, s, 7)
            else:
                pyxel.text(pyxel.width - self.border * 2, 20, s, 1)
                pyxel.text(pyxel.width - self.border * 2, 20, s, 7)

    def isProperHit(self, pY):
        if pY <= self.By <= pY + self.pLength:
            return True

        return False

    def handlePaddleCollision(self, pY):

        hasBallCollided = False

        # entering the realm of either left or right paddle
        if (self.BCoordinates["leftX"] <= self.p1x and self.vx < 0) or (self.BCoordinates["rightX"] >= self.p2x and self.vx > 0):

            if self.BCoordinates["bottomY"] < pY or self.BCoordinates["topY"] > pY + self.pLength:
                pass #missed
            else:
                pyxel.play(ch=0, snd=0)
                hasBallCollided = True

                self.logger.debug(f'Collided with paddle! Ball coordinates on hit: x is {self.Bx} and y is {self.By}')
                # determine angle of hit if not proper hit
                if not self.isProperHit(pY):
                    if self.vy > 0: #ball coming from top

                        if self.By < pY: # hitting top edge
                            self.logger.debug(f'ball coming from top, hit top edge of paddle with difference {abs(pY - self.By)}')
                            self.vy = self.vy * -1
                        else:
                            self.logger.debug(f'ball coming from top, hit bottom edge of paddle with difference {abs(pY - self.By)}')

                        self.vx = self.vx * -1
                        self.vx = abs(self.vx) - abs(pY - self.By) / 10
                    else: #ball coming from bottom

                        if self.By < pY: # hitting top edge
                            self.logger.debug(f'ball coming from bottom, hit top edge of paddle with difference {abs(pY - self.By)}')
                        else:
                            self.logger.debug(f'ball coming from bottom, hit bottom edge of paddle with difference {abs(pY - self.By)}')
                            self.vy = self.vy * -1

                        self.vx = self.vx * -1
                        self.vx = abs(self.vx) - abs(pY - self.By) / 10
                else:
                    self.logger.debug("proper hit!")
                    self.vx = self.vx * -1

        return hasBallCollided

    def checkGameEndScore(self):
        if self.p1Score == self.endGameScore or self.p2Score == self.endGameScore:
            self.hasGameEnded = True
            pyxel.play(ch=0, snd=2)

    def checkBallCollision(self):

        self.BCoordinates = {
            "topY": self.By - self.Br,
            "bottomY": self.By + self.Br,
            "leftX": self.Bx - self.Br,
            "rightX": self.Bx + self.Br
        }

        #top or down collision
        if self.BCoordinates["topY"] < 1 or self.BCoordinates["bottomY"] > pyxel.height - 1:
            self.vy = self.vy * -1

        ballHitP1 = self.handlePaddleCollision(self.p1y)
        ballHitP2 = self.handlePaddleCollision(self.p2y)

        if ballHitP1 or ballHitP2:
            self.hitCount += 1
            if self.hitCount > 1 and self.hitCount % self.increaseSpeedAfter == 0:
                self.logger.debug(f'Increasing speed after {self.hitCount} hits')
                self.vx = self.vx * self.increaseSpeedFactor
                self.vy = self.vy * self.increaseSpeedFactor

        # missed both
        if self.Bx > self.p2x:
            self.logger.debug("missed by p2!")
            self.p1Score += 1
            self.isRoundActive = False
            pyxel.play(ch=0, snd=1)
        elif self.Bx < self.p1x:
            self.logger.debug("missed by p1!")
            self.p2Score += 1
            self.isRoundActive = False
            pyxel.play(ch=0, snd=1)

    def updateControlKeys(self):
        if pyxel.btn(self.p1KeyUp):
            if self.p1y > 1:
                self.p1y = (self.p1y - self.pMovingDistance)

        if pyxel.btn(self.p1KeyDown):
            if self.p1y + self.pLength + self.pMovingDistance < pyxel.height - 1:
                self.p1y = (self.p1y + self.pMovingDistance)

        if pyxel.btn(self.p2KeyUp):
            if self.p2y > 1:
                self.p2y = (self.p2y - self.pMovingDistance)

        if pyxel.btn(self.p2KeyDown):
            if self.p2y + + self.pLength + self.pMovingDistance < pyxel.height - 1:
                self.p2y = (self.p2y + self.pMovingDistance)

App()
