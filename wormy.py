import random, pygame, sys
from pygame.locals import *
from pygame import font


FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window must be a multiple of cell size"
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the head 
# we have wormCoords[HEAD] the head of worms

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('freesansbold.ttf',18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()

def runGame():
    # set a random start point
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,  'y': starty},
                  {'x': startx - 1,  'y': starty},
                  {'x': startx - 2,  'y': starty}] # store worms
                   # segments into a dictionary
    direction = RIGHT

    # Start apple in random place
    apple = getRandomLocation()
    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_LEFT or event.key == K_a) and direction!= RIGHT:
                    direction = LEFT # direction is current direction
                elif(event.key == K_RIGHT or event.key == K_d) and direction!= LEFT:
                    direction = RIGHT
                elif(event.key == K_UP or event.key == K_w) and direction!= DOWN:
                    direction = UP
                elif(event.key == K_DOWN or event.key == K_s) and direction!= UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
    # Check collision
    if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH \
        or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT: # on edge
        return # gameover
    for wormBody in wormCoords[1:]:
        if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
            return # Game over
    # Check collision with apple
    if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
        # don't remove worms tail segment
        apple = getRandomLocation() # set a new apple
    else:
        del wormCoords[-1] # remove worm's tail segment
    if direction == UP:
        newHead = {'x': wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y']-1}
    elif direction == DOWN:
        newHead = {'x': wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y']+1}
    elif direction == LEFT:
        newHead = {'x': wormCoords[HEAD]['x']-1,'y':wormCoords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': wormCoords[HEAD]['x']+1,'y':wormCoords[HEAD]['y']}
    wormCoords.insert(0, newHead)
    # Drawing the screen
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    drawWorm(wormCoords)
    drawApple(apple)
    drawScore(len(wormCoords)-3)
    pygame.display.update()
    FPSCLOCK.tick(FPS)

# where to put apples
def getRandomLocation():
    return {'x': random.randint(0,CELLWIDTH-1), 'y': random.randint(0, CELLHEIGHT -1)}

# terminate game
def terminate():
    pygame.quit()
    sys.exit()

# Drawing 'press a key' screen
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topLeft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
        
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# The start screen
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degree1 = 0
    degrees = 0
    while True: # event loop
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degree1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degree1)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear out other events
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        degree1 += 3
        degree2 += 7

        
# Game over screen
def showGameOverScreen():
    gameOverFont = pygame.font.SysFont('freesansbold.ttf',150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()

    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

# Drawing things
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: s' % (score),True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120,10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x= coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x+4, y+4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRects)
        
        
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):#vertical
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0), (x,WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):#horizontal
        pygame.draw.line(DISPLAYSURF, DARKGRAY,(0,y),(WINDOWWIDTH,y))

# MAIN
if __name__ == '__main__':
    main()

    
        
