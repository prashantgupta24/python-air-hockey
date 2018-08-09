import pyxel

class App:
    def __init__(self):
        print("Starting game...")
        pyxel.init(200, 200)
        self.segmentLength = 20
        self.movingLength = 5 #pixels to move on key press
        self.border = 10

        self.l1x = 20
        self.l1y = pyxel.height / 2

        self.l2x = pyxel.width - 20
        self.l2y = pyxel.height / 2

        pyxel.run(self.update, self.draw)

    def update(self):
        #print("update")
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_W):
            if self.l1y - self.movingLength > self.border:
                self.l1y = (self.l1y - self.movingLength)

        if pyxel.btn(pyxel.KEY_S):
            if self.l1y + self.segmentLength + self.movingLength < pyxel.height-self.border:
                self.l1y = (self.l1y + self.movingLength)

        if pyxel.btn(pyxel.KEY_UP):
            if self.l2y - self.movingLength > self.border:
                self.l2y = (self.l2y - self.movingLength)

        if pyxel.btn(pyxel.KEY_DOWN):
            if self.l2y + + self.segmentLength + self.movingLength < pyxel.height-self.border:
                self.l2y = (self.l2y + self.movingLength)

    def draw(self):
        #print("draw")
        pyxel.cls(0)

        pyxel.line(self.l1x, self.l1y, self.l1x, self.l1y + self.segmentLength, 7)
        pyxel.line(self.l2x, self.l2y, self.l2x, self.l2y + self.segmentLength, 7)

App()
