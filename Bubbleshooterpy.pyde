# Libraries
import random
import time


# Variables



# TO BE FIXED
# - (!) Merging bubbles
# - Menu
# - Popanimation
# - New row mechanic
# - Canvas y size


class FlyingBubble:  # Flying Bubble class
    def __init__(self, game, x, y, xSlow, ySlow, xSpeed, ySpeed, size, val):
        self.game = game
        self.x = x
        self.y = y
        self.xSlow = xSlow
        self.ySlow = ySlow
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.size = size
        self.val = val
        self.dir = 1

    # Function to detect if flying bubble collided with stationary bubble
    def Collision(self, slow):
        if not slow:
            xComp = self.x
            yComp = self.y
        elif slow:
            xComp = self.xSlow
            yComp = self.ySlow

        if (yComp - self.game.bubbleSize) <= 4:
            return True

        row = int(round((yComp - self.game.colWidth) / (self.game.bubbleSize + 4)))
        if row > 15:
            row = 15
        elif row < 0:
            row = 0

        if self.game.rowIndent:
            if row % 2 == 0:
                self.game.rowWidth = 47
            else:
                self.game.rowWidth = 30

        else:
            if row % 2 == 0:
                self.game.rowWidth = 30
            else:
                self.game.rowWidth = 47

        col = int(round((xComp - self.game.rowWidth) / (self.game.bubbleSize + 4)))
        if col > 15:
            col = 15
        elif col < 0:
            col = 0

        relRow = -1
        while relRow <= 1:
            if (relRow + row) < 0 or (relRow + row) > 15:
                relRow += 1
                continue

            relCol = -1
            while relCol <= 1:
                if (relCol + col) < 0 or (relCol + col) > 15:
                    relCol += 1
                    continue
                statBubble = self.game.gridList[relRow + row][relCol + col]
                if statBubble != 0:
                    distX = xComp - statBubble.x
                    distY = yComp - statBubble.y
                    distance = sqrt((distX**2) + (distY**2))

                    if distance <= (self.game.bubbleSize - 4):
                        return True

                relCol += 1
            relRow += 1

        return False

    # Function to bounce off walls
    def ChangeDirection(self):
        if self.x < 26 or self.x > 563:  # FIX BOUNDS
            self.dir *= -1

    # Function to move bubble
    def Move(self):
        self.xSlow = self.x
        self.ySlow = self.y
        self.x += self.xSpeed * self.dir
        self.y += self.ySpeed

    # Function to slowly move the bubble after a collision detection
    def SlowMove(self):
        self.xSlow += self.xSpeed / self.game.bubbleFlySpeed * self.dir
        self.ySlow += self.ySpeed / self.game.bubbleFlySpeed

        if self.Collision(True):
            self.Teleport()

        else:
            self.SlowMove()

    # Function to display bubble
    def Display(self):
        self.game.ColorAssigner(self.val)
        stroke(1)
        ellipse(self.xSlow, self.ySlow, self.size, self.size)

    # Function to teleport bubble to nearest grid point
    def Teleport(self):
        self.game.currentBubble.remove(self)

        rowNew = int(round((self.ySlow - self.game.colWidth) / (self.game.bubbleSize + 4)))
        if rowNew > 15:
            rowNew = 15
        elif rowNew < 0:
            rowNew = 0

        if self.game.rowIndent:
            if rowNew % 2 == 0:
                self.game.rowWidth = 47
            else:
                self.game.rowWidth = 30

        else:
            if rowNew % 2 == 0:
                self.game.rowWidth = 30
            else:
                self.game.rowWidth = 47

        colNew = int(round((self.xSlow - self.game.rowWidth) / (self.game.bubbleSize + 4)))
        if colNew > 15:
            colNew = 15
        elif colNew < 0:
            colNew = 0

        if self.game.gridList[rowNew][colNew] != 0:
            print("Error, wanted to merge with:")
            print(colNew, rowNew)
            print(
                (self.xSlow - self.game.rowWidth) / (self.game.bubbleSize + 4),
                (self.ySlow - self.game.colWidth) / (self.game.bubbleSize + 4),
            )

        self.game.gridList[rowNew][colNew] = StatBubble(
            self.game,
            rowNew,
            colNew,
            (self.game.bubbleSize + 4) * colNew + self.game.rowWidth,
            (self.game.bubbleSize + 4) * rowNew + self.game.colWidth,
            self.val,
        )

        self.game.PopBubbles(self.game.gridList[rowNew][colNew])


class StatBubble:  # Stationary Bubble class
    def __init__(self, game, row, col, x, y, val):
        self.game = game
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.val = val

    def CheckNeighbours(self):
        neighbours = set()

        rowU = self.row - 1
        rowD = self.row + 1
        colL = self.col - 1
        colR = self.col + 1

        if rowU == -1:
            rowU = 0

        elif rowD == 16:
            rowD = 15

        if colL == -1:
            colL = 0

        elif colR == 16:
            colR = 15

        if self.row > 0:
            neighbours.add(self.game.gridList[rowU][self.col])  # Above

        if self.row < 15:
            neighbours.add(self.game.gridList[rowD][self.col])  # Below

        if self.col > 0:
            neighbours.add(self.game.gridList[self.row][colL])  # Left

            if (int(self.game.rowIndent == True) + self.row) % 2 == 0:  # Row Not Indented
                neighbours.add(self.game.gridList[rowU][colL])  # Left Above
                neighbours.add(self.game.gridList[rowD][colL])  # Left Below

        if self.col < 15:
            neighbours.add(self.game.gridList[self.row][colR])  # Right

            if (int(self.game.rowIndent == True) + self.row) % 2 != 0:  # Row Indented
                neighbours.add(self.game.gridList[rowU][colR])  # Right Above
                neighbours.add(self.game.gridList[rowD][colR])  # Right Below

        return neighbours

class Game:
    gridList = [[0] * 16 for _ in range(16)]
    colorsInGame = {1, 2, 3, 4, 5, 6}
    startPosition = PVector(302, 617)
    bubbleFlySpeed = 8
    currentBubble = []
    canShoot = True
    gameOver = False
    score = 69
    rowIndent = False
    colWidth = 30
    rowWidth = 47
    currentColor = random.choice(tuple(colorsInGame))
    nextColor = random.choice(tuple(colorsInGame))
    bubbleSize = 30
    spacing = 4
    iter = 0
    
    # def __init__(self):
    #     print("Game initialized")

    def setup(self):
        print("Game setup done")
        self.Start()

    def draw(self):  # Loopfunction
        # self.iter += 1
        # if (self.iter % 30 == 0):
        #     print(int(frameRate))

        if not self.gameOver:
            background(unhex("ffc1c0ff"))
            self.Initialize()
            self.DrawBubble()

        if mousePressed:
            mx = mouseX
            my = mouseY

            if my < 590 and my >= 10 and mx <= 580 and mx >= 10 and self.canShoot:
                self.FireBubble(mx, my)
                time.sleep(0.1)

            # elif for buttons

        if keyPressed:
            if key == " ":
                self.canShoot = True
            if key == "w":
                self.NewRow()
                time.sleep(0.1)
            if key == "r":
                self.gameOver = False
                self.canShoot = True
                colorsInGame = {1, 2, 3, 4, 5, 6}
                self.Start()
                time.sleep(0.1)
    
    def Initialize(self):  # Function to initialize the game
        strokeWeight(10)
        stroke(unhex("ffc1c0ff"))
        fill(255)
        rect(4, 4, 580, 641)

        strokeWeight(1)
        x = 10
        while x < 580:
            stroke(-(x + 590 >> 1 & 1))
            line(x, 590, x + 5, 590)
            x += 6

        fill(unhex("ffc1c0ff"))
        strokeWeight(1)
        stroke(unhex("ffc1c0ff"))
        rect(595, 0, 224, 649)

        strokeWeight(1.3)
        stroke(0)
        fill(0)

        for i, row in enumerate(self.gridList):
            if self.rowIndent:
                self.rowWidth = 47
                self.rowIndent = False

            else:
                self.rowWidth = 30
                self.rowIndent = True

            for j, statBubble in enumerate(row):
                if statBubble != 0:
                    statBubble.row = i
                    statBubble.col = j
                    statBubble.x = (self.bubbleSize + 4) * j + self.rowWidth
                    statBubble.y = (self.bubbleSize + 4) * i + self.colWidth
                    stroke(1)
                    self.ColorAssigner(statBubble.val)
                    ellipse(statBubble.x, statBubble.y, self.bubbleSize, self.bubbleSize)
    
    def Start(self):  # Function to fill the grid at the start of a game
        for row in range(9):
            if self.rowIndent:
                self.rowWidth = 47
                self.rowIndent = False

            else:
                self.rowWidth = 30
                self.rowIndent = True

            for col in range(16):
                self.gridList[row][col] = StatBubble(
                    self,
                    row,
                    col,
                    (self.bubbleSize + 4) * col + self.rowWidth,
                    (self.bubbleSize + 4) * row + self.colWidth,
                    random.choice(tuple(self.colorsInGame)),
                )

        for row in range(9, 16):
            for col in range(16):
                self.gridList[row][col] = 0

    def FireBubble(self, mouseX, mouseY):  # Function to fire bubbles
        xSpeed = 0
        ySpeed = 0
        self.canShoot = False
        angle = atan2(float(mouseY) - (self.startPosition.y), float(mouseX) - (self.startPosition.x))
        xSpeed = cos(angle)
        ySpeed = sin(angle)
        xSpeed *= self.bubbleFlySpeed
        ySpeed *= self.bubbleFlySpeed

        self.currentBubble.append(
            FlyingBubble(
                self,
                self.startPosition.x,
                self.startPosition.y,
                self.startPosition.x,
                self.startPosition.y,
                xSpeed,
                ySpeed,
                self.bubbleSize,
                self.currentColor,
            )
        )

    def DrawBubble(self):  # Function to draw the fired bubble every frame
        pushMatrix()
        translate(self.startPosition.x, self.startPosition.y)
        stroke(1)

        if self.canShoot:
            self.ColorAssigner(self.currentColor)
            ellipse(0, 0, self.bubbleSize, self.bubbleSize)

        self.ColorAssigner(self.nextColor)
        ellipse(-270, 0, self.bubbleSize, self.bubbleSize)
        popMatrix()

        for bubble in self.currentBubble:
            if bubble.Collision(False):
                bubble.SlowMove()
                self.canShoot = True

            else:
                bubble.ChangeDirection()
                bubble.Move()
                bubble.Display()

    def PopBubbles(self, firedBubble):  # Function to remove same colored and orphaned bubbles
        sameColor = {firedBubble}
        neighbourList = set()

        length = 0
        while len(sameColor) > length:
            length = len(sameColor)
            for bubble in sameColor:
                for neighbour in bubble.CheckNeighbours():
                    if neighbour != 0:
                        if neighbour.val == firedBubble.val:
                            sameColor.add(neighbour)
                        else:
                            neighbourList.add(neighbour)

        if length > 2:
            # Remove same colored bubbles
            for bubble in sameColor:
                # FIX: Popanimation
                self.gridList[bubble.row][bubble.col] = 0
                sameColor.remove(bubble)

            # Remove orphaned bubbles
            for bubble in neighbourList:
                length = 0
                recursiveList = {bubble}
                while len(recursiveList) > length:
                    length = len(recursiveList)
                    for neighbour in recursiveList:
                        for recNeighbour in neighbour.CheckNeighbours():
                            if recNeighbour != 0:
                                recursiveList.add(recNeighbour)

                attached = False
                for neighbour in recursiveList:
                    if neighbour.row == 0:
                        attached = True
                        break

                for neighbour in recursiveList:
                    if not attached:
                        self.gridList[neighbour.row][neighbour.col] = 0
                    neighbourList.discard(neighbour)

        self.CheckGameOver()
        self.currentColor = self.nextColor
        self.CheckColorsInGame()
        self.nextColor = random.choice(tuple(self.colorsInGame))
    def NewRow(self):  # Function to create new row in the grid
        # Creating new row
        if not self.gameOver:
            # Changing rowWidth if it should be indented
            if self.rowIndent:
                self.rowWidth = 47
                self.rowIndent = False

            else:
                self.rowWidth = 30
                self.rowIndent = True

            self.gridList.pop()
            tempRow = [0] * 16
            for col in range(16):
                tempRow[col] = StatBubble(
                    self,
                    0,
                    col,
                    (self.bubbleSize + 4) * col + self.rowWidth,
                    self.colWidth,
                    random.choice(tuple(self.colorsInGame)),
                )

            self.gridList.insert(0, tempRow)
        self.CheckGameOver() 


    def CheckColorsInGame(self):  # Function to check which colors are still in the game
        currentColorsInGame = set()

        for row in range(16):
            for col in range(16):
                if self.gridList[row][col] != 0:
                    currentColorsInGame.add(self.gridList[row][col].val)

        currentColorsInGame.add(self.currentColor)
        currentColorsInGame.add(self.nextColor)

        self.colorsInGame.clear()
        self.colorsInGame.update(currentColorsInGame)

    def CheckGameOver(self):  # Function to check if player is Game Over
        win = True
        for col in range(16):
            if self.gridList[15][col] != 0:
                self.gameOver = True
                self.canShoot = False
                print("lost")
                self.GameOverScreen("lost")
                break

            if self.gridList[0][col] != 0:
                win = False

        if win:
            self.gameOver = True
            self.canShoot = False
            self.GameOverScreen("win")

    def GameOverScreen(self, state):  # Function to display the Game Over screen
        if state == "win":
            background(0)
            fill(100, 100, 100)
            textFont(loadFont("TimesNewRomanPSMT-48.vlw"), 60)
            textAlign(CENTER, CENTER)
            text("YOU WON!", width / 2, height / 2)
            textFont(loadFont("TimesNewRomanPSMT-48.vlw"), 20)
            textAlign(CENTER, CENTER)
            text("(With a score of " + str(self.score) + ")", width / 2, 400)

        elif state == "lost":
            background(0)
            fill(79, 0, 0)
            textFont(loadFont("TimesNewRomanPSMT-48.vlw"), 60)
            textAlign(CENTER, CENTER)
            text("YOU DIED", width / 2, height / 2)
            textFont(loadFont("TimesNewRomanPSMT-48.vlw"), 20)
            textAlign(CENTER, CENTER)
            text("(With a score of " + str(self.score) + ")", width / 2, 400)

    def ColorAssigner(self, value):  # Function to decode values into hexes
        if value == 0:
            pass

        elif value == 1:
            # Red: ffef161a
            fill(unhex("ffef161a"))

        elif value == 2:
            # Green: ff00da00
            fill(unhex("ff00da00"))

        elif value == 3:
            # Yellow: fffeff00
            fill(unhex("fffeff00"))

        elif value == 4:
            # Purple: ffe500e6
            fill(unhex("ffe500e6"))

        elif value == 5:
            # Dark Blue: ff1e00fd
            fill(unhex("ff1e00fd"))

        elif value == 6:
            # Light Blue: ff02fafa
            fill(unhex("ff02fafa"))

        else:
            raise Exception("Encountered value " + str(value) + " while initializing")

game = Game()
def setup():
    size(800, 650)
    ellipseMode(CENTER)
    smooth()
    frameRate(160)
    clear()
    game.setup()
def draw():
    game.draw()