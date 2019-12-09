'''import pygame, math, random, time
import audio_processing_version2 as ad

pygame.init()

class RunGame(object):
    def __init__(self, width, height,time):
        self.initGame(width,height)
        self.preloadAudio()


    def playMusic(self):
        pygame.mixer.music.load(self.musicFileName)
        pygame.mixer.music.play(0)
        self.startTime = self.time.time()

    def generateRect(self):
        self.currentTime = self.time.time()
        timePassed = round(self.currentTime - self.startTime,1)
        for time in self.musicAmpList:
            if timePassed == time - self.timeDelay:
                #print(timePassed,'shit')
                rect = self.getNewRectangle()
                self.rectangleGroup.add(self.getNewRectangle())

    def initGame(self,width,height):
        self.screenWidth = width
        self.screenHeight = height
        self.screen = pygame.display.set_mode((width, height))
        self.canvas = pygame.Surface((width, height)).convert()
        self.canvas.fill((0, 0, 0))
        pygame.font.init()
        self.waiting = True
        self.line = Player(self.screenWidth/2, self.screenHeight/2) # the line that the player owns
        self.bg = Background(0.3, self.screenWidth) # the red line background
        self.rectangleGroup = pygame.sprite.Group()
        self.counterClock = False
        self.clockwise = False
        self.running = True
        self.selectionMode = True
        self.time = time
        self.globalTime = time.time()
        self.timeDelay = 0
        self.score = 0

    def preloadAudio(self):
        self.audioDict = ad.audio_extract()

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.counterClock = True
                    self.clockwise = False
                elif event.key == pygame.K_RIGHT:
                    self.counterClock = False
                    self.clockwise = True
                elif event.key == pygame.K_SPACE:
                    self.rectangleGroup.add(self.getNewRectangle())
            elif event.type == pygame.KEYUP:
                if (self.counterClock and event.key == pygame.K_LEFT):
                    self.counterClock = False
                elif (self.clockwise and event.key == pygame.K_RIGHT):
                    self.clockwise = False

    def updateGame(self):
        self.doRotate()
        self.rectangleGroup.update()
        self.isCollide()
        self.removeRectangle()

    def getNewRectangle(self):
        direction = random.choice(['N','S','W','E'])
        return Rectangle(direction, self.bg)

    def isCollide(self):
        x1, y1 = self.line.x1, self.line.y1
        x2, y2 = self.line.x2, self.line.y2
        for rectangle in self.rectangleGroup:
            if (not rectangle.ischecked and
            (rectangle.x0 < 0 or rectangle.x0 > self.screenWidth or
            rectangle.y0 < 0 or rectangle.y0 > self.screenHeight)):
                rectangle.ischecked = True
                if (rectangle.rect[0] < x1 < rectangle.rect[0]+rectangle.rect[2] and
            rectangle.rect[1] < y1 < rectangle.rect[1]+rectangle.rect[3]):
                    self.score += 1
                elif (rectangle.rect[0] < x2 < rectangle.rect[0]+rectangle.rect[2] and
                rectangle.rect[1] < y2 < rectangle.rect[1]+rectangle.rect[3]):
                    self.score += 1

    def removeRectangle(self):
        for rectangle in self.rectangleGroup:
            if ((rectangle.direction == 'N' and rectangle.y0+rectangle.rect[3]<0) or
            (rectangle.direction == 'S' and rectangle.y0-rectangle.rect[3] > self.screenHeight) or
            (rectangle.direction == 'W' and rectangle.x0+rectangle.rect[2]<0) or
            (rectangle.direction == 'E' and rectangle.x0-rectangle.rect[2]> self.screenWidth)):
                self.rectangleGroup.remove(rectangle)

    def doRotate(self):
        if self.counterClock:
            self.line.rotate('counterClock')
        elif self.clockwise:
            self.line.rotate('clockwise')
        elif self.line.omega != 0:
            self.line.rotate()

    def redrawAll(self):
        WHITE = (255,255,255)
        self.screen.blit(self.canvas, (0, 0))
        self.bg.draw(self.screen)
        self.rectangleGroup.draw(self.screen)
        self.line.draw(self.screen)
        font = pygame.font.SysFont('Current Score', 50)
        text = font.render(f'{self.score}', True, WHITE)
        self.screen.blit(text, (self.screenWidth/2-15, self.screenHeight/2-5))
        pygame.display.update()

    def waitForKey(self):
        waiting = True
        while waiting:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    waiting = False

    def showStartScreen(self):
        # 画一下这个基本的splash screen
        #self.screen.blit(self.canvas, (0, 0))
        WHITE = (255, 255, 255)
        DARKBLUE = (93, 96, 142)
        self.screen.fill(DARKBLUE)
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text1 = font.render('GBAR Music', True, WHITE)
        text2 = font.render('Press Any Key To Enter',True,WHITE)
        self.screen.blit(text1, (170,180))
        self.screen.blit(text2, (90,250))
        pygame.display.update()
        self.waitForKey()

    def showSelectionMode(self):
        WHITE = (255, 255, 255)
        DARKBLUE = (93, 96, 142)
        self.screen.fill(DARKBLUE)
        font = pygame.font.SysFont('Comic Sans MS', 25)
        text1 = font.render('Select the Music to Play...', True, WHITE)
        self.screen.blit(text1, (20,180))
        #pygame.display.update()

        tempDict = dict()
        counter = 0
        vertSpace = 30
        for element in self.audioDict:
            tempDict[element] = [font.render(f'{element}',True,WHITE),(40, 210 + counter*vertSpace)]
            counter += 1
        for element in tempDict:
            self.screen.blit(tempDict[element][0], tempDict[element][1])
            pygame.display.update()

        self.musicSelected = self.selectionEventHandler(tempDict,vertSpace)
        self.musicFileName = str(self.musicSelected) + '.wav'
        self.musicAmpList = self.audioDict[self.musicSelected]
        # print('Hello cyka ', self.musicSelected, type(self.musicSelected))
        self.selectionMode = False

    def selectionEventHandler(self, tempDict, vertSpace):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for element in tempDict:
                        if (tempDict[element][1][1]-vertSpace < pos[1] <
                                        tempDict[element][1][1]+vertSpace):
                                        return element

    def checkGameOver(self):
        currentTime = time.time()
        if currentTime - self.globalTime > self.audioDict[self.musicSelected][-1] + 5:
            self.running = False

    def drawGameOver(self):
        # 画一下这个基本的splash screen
        #self.screen.blit(self.canvas, (0, 0))
        WHITE = (255, 255, 255)
        DARKBLUE = (93, 96, 142)
        self.screen.fill(DARKBLUE)
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text1 = font.render('GameOver', True, WHITE)
        text2 = font.render('Press Space to restart',True,WHITE)
        self.screen.blit(text1, (170,180))
        self.screen.blit(text2, (90,250))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.initGame(self.screenWidth, self.screenHeight)
                        main()


class Background(object):
    def __init__(self, ratio, width):
        self.ratio = ratio
        self.screenL = width
        self.squareL = self.screenL * self.ratio
        self.screenTri = self.screenL/3
        self.squareTri = self.squareL/3
        self.cx = self.screenL/2
        self.cy = self.screenL/2
        self.cr = self.squareL * 0.5
        self.color = (100,100,100)
        self.width = 5

    def draw(self,screen):
        #draw rectangle
        pygame.draw.rect(screen, self.color, ((self.cx-self.cr,self.cy-self.cr)
        ,(self.squareL,self.squareL)), 5)
        for i in range(3):
            if i == 0:
                self.width = 5
            else:
                self.width = 1
            #draw top left line
            pygame.draw.line(screen, self.color, (0+self.screenTri*i,0), (self.cx-self.cr+self.squareTri*i,self.cy-self.cr), self.width)
            #draw top right line
            pygame.draw.line(screen, self.color, (self.screenL,0+self.screenTri*i),(self.cx+self.cr,self.cy-self.cr+self.squareTri*i), self.width)
            #draw down left line
            pygame.draw.line(screen, self.color, (0,self.screenL-self.screenTri*i),(self.cx-self.cr,self.cy+self.cr-self.squareTri*i), self.width)
            #draw down right line
            pygame.draw.line(screen, self.color, (self.screenL-self.screenTri*i,self.screenL),(self.cx+self.cr-self.squareTri*i,self.cy+self.cr),self.width)

class Player(object):
    def __init__(self, x, y):
        self.cx = x
        self.cy = y
        self.r = 250
        self.x1, self.y1 = self.cx-self.r, self.cy
        self.x2, self.y2 = self.cx+self.r, self.cy

        self.alpha = (5)*math.pi/180 # angular acceleration
        self.omega = 0 # angular speed
        self.theta = 0 # swiped angle

    def rotate(self, direction=None):
        maxOmega = 15*math.pi/180
        if direction == 'counterClock':
            self.omega = min(self.omega+self.alpha, maxOmega)
        elif direction == 'clockwise':
            self.omega = max(self.omega-self.alpha, -maxOmega)
        else:
            if self.omega < 0:
                self.omega = min(self.omega+self.alpha, 0)
            elif self.omega > 0:
                self.omega = max(self.omega-self.alpha, 0)
        self.theta = (self.theta+self.omega)%(2*math.pi)
        self.x1 = self.cx+self.r*math.cos(self.theta+math.pi)
        self.y1 = self.cy-self.r*math.sin(self.theta+math.pi)
        self.x2 = self.cx+self.r*math.cos(self.theta)
        self.y2 = self.cy-self.r*math.sin(self.theta)

    def draw(self, screen):
        pygame.draw.line(screen, (255,0,0),
        (self.x1, self.y1), (self.x2, self.y2), 5) # 5 is width

class Rectangle(pygame.sprite.Sprite):
    def __init__(self,direction,bg):
        super().__init__()
        self.direction = direction
        (self.theta, self.signs, self.x0, self.y0, self.x1, self.y1) = self.getBeginning(bg)
        self.rect = self.getRect()
        self.w0 = self.rect[2]
        self.color = (0, 255, 0)
        self.image = pygame.Surface((self.rect[2], self.rect[3]))
        self.image.fill(self.color)
        self.v0 = 10
        self.ischecked = False

    def getBeginning(self,bg):
        if self.direction in ['N', 'S']:
            theta = math.atan(3)
            if self.direction == 'N':
                signs = [-1, -1, +1, -1]
            elif self.direction == 'S':
                signs = [-1, +1, +1, +1]
            dirX = 1/3
            dirY = 1
        elif self.direction in ['W', 'E']:
            theta = math.pi/2-math.atan(3)
            if self.direction == 'W':
                signs = [-1, -1, -1, +1]
            elif self.direction == 'E':
                signs = [+1, -1, +1, +1]
            dirX = 1
            dirY = 1/3
        # calculate start and end points
        x0 = bg.cx + signs[0]*bg.cr*dirX
        y0 = bg.cy + signs[1]*bg.cr*dirY
        x1 = bg.cx + signs[2]*bg.cr*dirX
        y1 = bg.cy + signs[3]*bg.cr*dirY
        return theta, signs, x0, y0, x1, y1

    def getRect(self):
        ratio = 0.5 # ratio of height/width
        if self.direction in ['N', 'S']:
            w = self.x1-self.x0
            h = w*ratio
            if self.direction == 'N':
                rect = (self.x0, self.y0, w, h)
            elif self.direction == 'S':
                rect = (self.x0, self.y0-h, w, h)
        elif self.direction in ['W', 'E']:
            w = self.y1-self.y0
            h = w*ratio
            if self.direction == 'W':
                rect = (self.x0, self.y0, h, w)
            elif self.direction == 'E':
                rect = (self.x0-h, self.y0, h, w)
        return rect

    def update(self):
        self.v = self.v0*self.rect[2]/self.w0
        dx0 = self.signs[0]*self.v*math.cos(self.theta)
        dy0 = self.signs[1]*self.v*math.sin(self.theta)
        dx1 = self.signs[2]*self.v*math.cos(self.theta)
        dy1 = self.signs[3]*self.v*math.sin(self.theta)
        # print(dx0, dx1)
        # print(dy0, dy1)
        self.x0 += dx0
        self.y0 += dy0
        self.x1 += dx1
        self.y1 += dy1
        # print(int(self.x0), int(self.y0))
        self.rect = self.getRect()
        self.image = pygame.Surface((self.rect[2], self.rect[3]))
        self.image.fill(self.color)

    def draw(self, screen):
        #draw the rectangle
        # pygame.draw.rect(screen, self.color,self.rect, 3)
        # print('drawing')
        screen.blit(self.image, self.rect, self.rect)

class RunSplash(object):
    def __init__(self, width, height):
        super().__init__(width, height)

def main(g = RunGame(500,500,time)):
    g.showStartScreen()
    while g.running:
        pygame.time.delay(50)
        if g.selectionMode:
            g.showSelectionMode() ############
            g.playMusic()
        g.checkGameOver()
        g.generateRect()
        g.eventHandler()
        g.updateGame()
        g.redrawAll()
    g.drawGameOver()
'''
