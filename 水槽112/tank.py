################################################################################
'''
Initialization Stuff:
• This sets up everything we need for the rest of the game.

StackOverFlow References:
• https://stackoverflow.com/questions/62543965/pygame-audio-error-unrecognized
-audio-format
'''
################################################################################

from cmu_112_graphics import *
from bfsAlgo import *
from collide import *
from pygame import mixer
import random

'''
All use of pygame was guided by: 
https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
and documentation of the mixer module:
https://www.pygame.org/docs/ref/mixer.html
'''
mixer.init()
mixer.music.load('title.ogg')
# This song is 'Field Theme 01' from the game MOTHER for the NES.
mixer.music.play(-1)
createAdjList()
collisionBuilder()

class fish:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        spawnNodes = set(adjList) - collisions
        self.locationNode = random.choice(list(spawnNodes)) 
        self.locationCoords = nodeToCoord(self.locationNode)
        self.currentNode = coordToNode(self.locationCoords)
        self.prevLocation = [None, None]
        self.health = 1

David = fish('David', random.choice(['carp', 'anchovy', 'tuna', 'sturgeon', 
        'rainbow']))
Mike = fish('Mike', random.choice(['carp', 'anchovy', 'tuna', 'sturgeon', 
        'rainbow']))
Aidan = fish('Aidan', random.choice(['carp', 'anchovy', 'tuna', 'sturgeon', 
        'rainbow']))

################################################################################
'Model'
################################################################################

def appStarted(app):
    app.timerDelay = 500
    # Boolean Flags and Fish Stuff
    app.dy = 20
    app.foodOffset = None
    app.startPage = True
    app.instructions = False
    app.playing = False
    app.statuses = False
    app.time = -1
    app.collisionNodes = collisions
    app.collisions = [nodeToCoord(node) for node in app.collisionNodes]
    app.foodCount = 0
    app.foodLocation = [None, None]
    app.foodDropped = False
    if app.foodDropped:
        app.foodNode = coordToNode(app.foodLocation)
    app.foodNode = None
    app.foodGoal = [None, None]
    app.foodCols = [None, 22, 24, 28, 19, 19, 19, 14, 13, 19, 15, 15, 17, 18, 
    18, 18, 18, 18, 30, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 11, 8, 9, 10, 
    16, 35, 35, 35, 33, 33, 32, 17, 17, 16, 14, 14, 12, 12, 13, 12, 12, 19, 19, 
    21, 21, 22, 22, 24, 28, 19, 19, 19]
    app.foodPath = {0:[], 1:[], 2:[]}
    app.fishList = [David, Mike, Aidan]
    app.randomlyMoving = True
    app.eating = False
    app.goalReached = False
    # Title Screen
    titleScreen = 'titleScreen.png'
    app.titleScreen = app.loadImage(titleScreen)
    # Instructions
    instructions = 'instructions.png'
    app.instructionsPage = app.loadImage(instructions)
    # Anchovy 
    '''Initial sprite taken from 
        https://stardewvalleywiki.com/mediawiki/images/7/79/Anchovy.png'''
    anchovy = 'anchovy.png'
    app.anchovyInit = app.loadImage(anchovy)
    app.anchovyRight = app.anchovyInit.rotate(-50)
    app.anchovyUp = app.anchovyInit.rotate(50)
    anchovyR = 'anchovyR.png'
    app.anchovyInitR = app.loadImage(anchovyR)
    app.anchovyLeft = app.anchovyInitR.rotate(45)
    app.anchovyDown = app.anchovyInitR.rotate(135)         
    # Carp
    '''Initial sprite taken from 
        https://stardewvalleywiki.com/mediawiki/images/a/a8/Carp.png'''
    carp = 'carp.png'
    app.carpInit = app.loadImage(carp)
    app.carpRight = app.carpInit.rotate(-45)
    app.carpUp = app.carpInit.rotate(45)
    carpR = 'carpR.png'
    app.carpInitR = app.loadImage(carpR)
    app.carpLeft = app.carpInitR.rotate(45)
    app.carpDown = app.carpInitR.rotate(135)
    # Rainbow
    '''Initial sprite taken from 
        https://stardewvalleywiki.com/mediawiki/images/1/14/Rainbow_Trout.png'''
    rainbow = 'rainbow.png'
    app.rainbowInit = app.loadImage(rainbow)
    app.rainbowRight = app.rainbowInit.rotate(-50)
    app.rainbowUp = app.rainbowInit.rotate(45)
    rainbowR = 'rainbowR.png'
    app.rainbowInitR = app.loadImage(rainbowR)
    app.rainbowLeft = app.rainbowInitR.rotate(50)
    app.rainbowDown = app.rainbowInitR.rotate(140)
    # Sturgeon
    '''Initial sprite taken from
        https://stardewvalleywiki.com/mediawiki/images/4/42/Sturgeon.png'''
    sturgeon = 'sturgeon.png'
    app.sturgeonInit = app.loadImage(sturgeon)
    app.sturgeonRight = app.sturgeonInit.rotate(-45)
    app.sturgeonUp = app.sturgeonInit.rotate(45)
    sturgeonR = 'sturgeonR.png'
    app.sturgeonInitR = app.loadImage(sturgeonR)
    app.sturgeonLeft = app.sturgeonInitR.rotate(45)
    app.sturgeonDown = app.sturgeonInitR.rotate(135)
    # Tuna
    '''Initial sprite taken from
        https://stardewvalleywiki.com/mediawiki/images/c/c5/Tuna.png'''
    tuna = 'tuna.png'
    app.tunaInit = app.loadImage(tuna)
    app.tunaRight = app.tunaInit.rotate(-45)
    app.tunaUp = app.tunaInit.rotate(45)
    tunaR = 'tunaR.png'
    app.tunaInitR = app.loadImage(tunaR)
    app.tunaLeft = app.tunaInitR.rotate(45)
    app.tunaDown = app.tunaInitR.rotate(135)
    # Food
    '''Initial sprite taken from
        https://stardewvalleywiki.com/mediawiki/images/7/70/Cookie.png'''
    food = 'food.png'
    app.food = app.loadImage(food)
    # Dimensions 
    app.width = 600
    app.height = 400
    app.rows = app.height//10
    app.cols = app.width//10
    app.margin = 0
    # Tank Images
    sand = 'https://pngimg.com/uploads/sand/sand_PNG30.png'
    app.sand = app.loadImage(sand)
    seaweed = 'seaweed.png'
    '''Original image taken from
        https://www.subpng.com/png-4qeon2/'''
    app.seaweedInit = app.loadImage(seaweed)
    app.seaweed = app.scaleImage(app.seaweedInit, 1/5)
    kelp = 'kelp.png'
    '''Original image taken from:
        https://www.walmart.com/ip/Artificial-Green-Seaweed-Vivid-Water-Plants-
        Plastic-Fish-Tank-Plant-Decorations-for-Aquarium/739618531'''
    app.kelpInit = app.loadImage(kelp)
    app.kelp = app.scaleImage(app.kelpInit, 1/5)
    dragon = 'dragon.png'
    '''Original image taken from:
        https://pangearocks.com/our-offer/aquariums/kelp-marine-plants%E2%80%8B/'''
    app.dragonInit = app.loadImage(dragon)
    app.dragon = app.scaleImage(app.dragonInit, 3/4)
    coral = 'coral.png'
    '''Original image taken from:
        https://picsart.com/i/sticker-267397817021211'''
    app.coralInit = app.loadImage(coral)
    app.coral = app.scaleImage(app.coralInit, 4/10)

def placeFood(app):
    x = random.randint(1, 60) 
    y = app.foodCols[x]
    app.foodLocation = [x * 10, 10]
    app.foodGoal = [x * 10, y * 10 - 20]

def isLegalMove(app, axis, move, other):
    if axis == 'x':
        if 20 <= move < app.width:
            if [move, other] not in app.collisions:
                return True
    if axis == 'y':
        if 10 < move < app.height - 40:
            if [other, move] not in app.collisions:
                return True
    return False

################################################################################
'Controller'
################################################################################

def timerFired(app): 
    #app.time += 1
    if app.foodCount == 0:
        app.fishOffset = None
        app.dy = 20
        app.time = -1
        app.eating = False
        app.foodDropped = False
        app.randomlyMoving = True
        app.foodPath = {0:[], 1:[], 2:[]}
        #app.fishList[0].locationCoords = app.fishList[0].locationCoords
        directions = [-20, 20]
        for fish in app.fishList:
            axis = random.choice(['x', 'y'])
            move = random.choice(directions)
            if axis == 'x':
                other = fish.locationCoords[1]
                newMove = fish.locationCoords[0] + move
                if isLegalMove(app, axis, newMove, other):
                    fish.prevLocation = fish.locationCoords
                    fish.locationCoords = [newMove, other]
            if axis == 'y':
                other = fish.locationCoords[0]
                newMove = fish.locationCoords[1] + move
                if isLegalMove(app, axis, newMove, other):
                    fish.prevLocation = fish.locationCoords
                    fish.locationCoords = [other, newMove]
    if app.eating and app.foodDropped:
        app.foodNode = coordToNode(app.foodGoal)
        app.foodPath[0] = [nodeToCoord(node) for node in bfs(adjList, 
                        app.fishList[0].currentNode, app.foodNode)]
        app.foodPath[1] = [nodeToCoord(node) for node in bfs(adjList, 
                        app.fishList[1].currentNode, app.foodNode)]
        app.foodPath[2] = [nodeToCoord(node) for node in bfs(adjList, 
                        app.fishList[2].currentNode, app.foodNode)]
        if app.eating:
            app.time += 1
            print(f'app.time = {app.time}')
            if app.time < len(app.foodPath[0]):
                app.fishList[0].locationCoords = app.foodPath[0][app.time]
                print(f'fish1 is at {app.fishList[0].locationCoords}')
                print(f'fish1 wants to go to {app.foodPath[0][app.time]}')
                print(app.foodPath[0])
            if app.time < len(app.foodPath[1]):
                app.fishList[1].locationCoords = app.foodPath[1][app.time]
                print(f'fish2 is at {app.fishList[1].locationCoords}')
                print(f'fish2 wants to go to {app.foodPath[1][app.time]}')
                print(app.foodPath[1])
            if app.time < len(app.foodPath[2]):
                app.fishList[2].locationCoords = app.foodPath[2][app.time]
                print(f'fish3 is at {app.fishList[2].locationCoords}')
                print(f'fish3 wants to go to {app.foodPath[2][app.time]}')
                print(app.foodPath[2])
            if app.fishList[0].locationCoords == app.foodPath[0][len(app.foodPath[0]) - 1]:
                if app.fishList[0].health < 10:
                    app.fishList[0].health += 1
                if app.fishList[1].health > 0:
                    app.fishList[1].health -= 1
                if app.fishList[2].health > 0:
                    app.fishList[2].health -= 1
                app.eating = False
                app.foodCount = 0
            if app.fishList[1].locationCoords == app.foodPath[1][len(app.foodPath[1]) - 1]:
                if app.fishList[1].health < 10:
                    app.fishList[1].health += 1
                if app.fishList[0].health > 0:
                    app.fishList[0].health -= 1
                if app.fishList[2].health > 0:
                    app.fishList[2].health -= 1
                app.eating = False
                app.foodCount = 0
            if app.fishList[2].locationCoords == app.foodPath[2][len(app.foodPath[2]) - 1]:
                if app.fishList[2].health < 10:
                    app.fishList[2].health += 1
                if app.fishList[0].health > 0:
                    app.fishList[0].health -= 1
                if app.fishList[1].health > 0:
                    app.fishList[1].health -= 1 
                app.eating = False
                app.foodCount = 0
    if app.foodCount == 1:
        app.randomlyMoving = True
        app.foodOffset = app.foodGoal[1] - app.foodLocation[1]
        if app.foodLocation[1] <= app.foodGoal[1]:
            if app.foodOffset < (app.foodGoal[1] - 10)/3: 
                app.dy = 20
            if (app.foodGoal[1] - 10)/3 <= app.foodOffset < (app.foodGoal[1] - 10)/2: 
                app.dy = 10
            if app.foodOffset <= (app.foodGoal[1] - 10)/2: 
                app.dy = 5
            app.foodLocation = [app.foodLocation[0], app.foodLocation[1] + app.dy]
        if app.foodLocation[1] >= app.foodGoal[1]:
            app.foodDropped = True
    if app.randomlyMoving:
        directions = [-20, 20]
        for fish in app.fishList:
            axis = random.choice(['x', 'y'])
            move = random.choice(directions)
            if axis == 'x':
                other = fish.locationCoords[1]
                newMove = fish.locationCoords[0] + move
                if isLegalMove(app, axis, newMove, other):
                    fish.prevLocation = fish.locationCoords
                    fish.locationCoords = [newMove, other]
            if axis == 'y':
                other = fish.locationCoords[0]
                newMove = fish.locationCoords[1] + move
                if isLegalMove(app, axis, newMove, other):
                    fish.prevLocation = fish.locationCoords
                    fish.locationCoords = [other, newMove]

def keyPressed(app, event):
    if event.key in ['F', 'f']:
        if app.foodDropped:
            return
        app.foodCount = 1
        app.eating = True
        placeFood(app)
    if event.key == 'Right':
        mixer.music.stop()
        mixer.music.load('game.wav')
        # This song is 'O2 in Love' from the game MOTHER 3 for the GBA.
        mixer.music.play(-1)
        app.instructions = False
        app.playing = True
    if event.key in ['S', 's']:
        app.statuses = True
    if event.key == 'Escape':
        if app.statuses:
            app.statuses = False

def mousePressed(app, event):
    if app.startPage:
        if (0 <= event.x <= app.width):
            app.startPage = False
            app.instructions = True
            mixer.music.stop()
            mixer.music.load('instructions.wav')
            mixer.music.play(-1)
    spawnNodes = set(adjList) - collisions
    if not app.eating:
        for fish in app.fishList:
            x = fish.locationCoords[0]
            y = fish.locationCoords[1]
            if (x - 30 <= event.x <= x + 30) and (y - 20 <= event.y <= y + 20):
                fish.locationCoords = nodeToCoord(random.choice(list(spawnNodes)))

def appStopped(app):
    mixer.music.stop()

################################################################################
'View'
################################################################################

def drawWater(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'dodger blue')

def drawSand(app, canvas):
    canvas.create_image(app.width/6, 6*app.height/7, 
    image=ImageTk.PhotoImage(app.sand))

def drawKelp(app, canvas):
    canvas.create_image(3.25*app.width/16, 5*app.height/6, 
    image=ImageTk.PhotoImage(app.kelp))
    canvas.create_image(2*app.width/8, 4*app.height/6, 
    image=ImageTk.PhotoImage(app.kelp))

def drawSeaweed(app, canvas):
    canvas.create_image(6*app.width/8, 4*app.height/6, 
    image=ImageTk.PhotoImage(app.seaweed))

def drawDragon(app, canvas):
    canvas.create_image(app.width/2, 5*app.height/6, 
    image=ImageTk.PhotoImage(app.dragon))

def drawCoral(app, canvas):
    canvas.create_image(0, 5*app.height/6, image=ImageTk.PhotoImage(app.coral))
    canvas.create_image(9*app.width/10, 5*app.height/6, 
    image=ImageTk.PhotoImage(app.coral))

def drawAnchovy(app, canvas, fish):
    currLocation = fish.locationCoords
    prevLocation = fish.prevLocation
    if currLocation[0] != prevLocation[0]:
        # The fish is moving right
        if (currLocation[0] - prevLocation[0]) > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.anchovyRight))
        # The fish is moving left
        if (currLocation[0] - prevLocation[0]) < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.anchovyLeft))
    if currLocation[1] != prevLocation[1]:
        # The fish is moving down
        if currLocation[1] - prevLocation[1] > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.anchovyDown))
        # The fish is moving up
        if currLocation[1] - prevLocation[1] < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.anchovyUp))
    if currLocation == prevLocation or (currLocation[0] != prevLocation[0] and currLocation[1] != prevLocation[1]):
        canvas.create_image(currLocation[0], currLocation[1], 
        image=ImageTk.PhotoImage(app.anchovyInit))

def drawCarp(app, canvas, fish):
    currLocation = fish.locationCoords
    prevLocation = fish.prevLocation
    if currLocation[0] != prevLocation[0]:
        # The fish is moving right
        if (currLocation[0] - prevLocation[0]) > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.carpRight))
        # The fish is moving left
        if (currLocation[0] - prevLocation[0]) < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.carpLeft))
    if currLocation[1] != prevLocation[1]:
        # The fish is moving down
        if currLocation[1] - prevLocation[1] > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.carpDown))
        # The fish is moving up
        if currLocation[1] - prevLocation[1] < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.carpUp))
    if currLocation == prevLocation or (currLocation[0] != prevLocation[0] and currLocation[1] != prevLocation[1]):
        canvas.create_image(currLocation[0], currLocation[1], 
        image=ImageTk.PhotoImage(app.carpInit))

def drawRainbow(app, canvas, fish):
    currLocation = fish.locationCoords
    prevLocation = fish.prevLocation
    if currLocation[0] != prevLocation[0]:
        # The fish is moving right
        if (currLocation[0] - prevLocation[0]) > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.rainbowRight))
        # The fish is moving left
        if (currLocation[0] - prevLocation[0]) < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.rainbowLeft))
    if currLocation[1] != prevLocation[1]:
        # The fish is moving down
        if currLocation[1] - prevLocation[1] > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.rainbowDown))
        # The fish is moving up
        if currLocation[1] - prevLocation[1] < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.rainbowUp))
    if currLocation == prevLocation or (currLocation[0] != prevLocation[0] and currLocation[1] != prevLocation[1]):
        canvas.create_image(currLocation[0], currLocation[1], 
        image=ImageTk.PhotoImage(app.rainbowInit))

def drawSturgeon(app, canvas, fish):
    currLocation = fish.locationCoords
    prevLocation = fish.prevLocation
    if currLocation[0] != prevLocation[0]:
        # The fish is moving right
        if (currLocation[0] - prevLocation[0]) > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.sturgeonRight))
        # The fish is moving left
        if (currLocation[0] - prevLocation[0]) < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.sturgeonLeft))
    if currLocation[1] != prevLocation[1]:
        # The fish is moving down
        if currLocation[1] - prevLocation[1] > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.sturgeonDown))
        # The fish is moving up
        if currLocation[1] - prevLocation[1] < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.sturgeonUp))
    if currLocation == prevLocation or (currLocation[0] != prevLocation[0] and currLocation[1] != prevLocation[1]):
        canvas.create_image(currLocation[0], currLocation[1], 
        image=ImageTk.PhotoImage(app.sturgeonInit))

def drawTuna(app, canvas, fish):
    currLocation = fish.locationCoords
    prevLocation = fish.prevLocation
    if currLocation[0] != prevLocation[0]:
        # The fish is moving right
        if (currLocation[0] - prevLocation[0]) > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.tunaRight))
        # The fish is moving left
        if (currLocation[0] - prevLocation[0]) < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.tunaLeft))
    if currLocation[1] != prevLocation[1]:
        # The fish is moving down
        if currLocation[1] - prevLocation[1] > 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.tunaDown))
        # The fish is moving up
        if currLocation[1] - prevLocation[1] < 0:
            canvas.create_image(currLocation[0], currLocation[1], 
            image=ImageTk.PhotoImage(app.tunaUp))
    if currLocation == prevLocation or (currLocation[0] != prevLocation[0] and currLocation[1] != prevLocation[1]):
        canvas.create_image(currLocation[0], currLocation[1], 
        image=ImageTk.PhotoImage(app.tunaInit))

def drawFish(app, canvas):
    for fish in app.fishList:
        if fish.species == 'anchovy':
            drawAnchovy(app, canvas, fish)
        if fish.species == 'carp':
            drawCarp(app, canvas, fish)
        if fish.species == 'rainbow':
            drawRainbow(app, canvas, fish)
        if fish.species == 'sturgeon':
            drawSturgeon(app, canvas, fish)
        if fish.species == 'tuna':
            drawTuna(app, canvas, fish)

def drawFood(app, canvas, x, y):
    canvas.create_image(x, y, image=ImageTk.PhotoImage(app.food))

def drawTest(app, canvas):
    canvas.create_image(app.width//2, app.height//2, 
    image=ImageTk.PhotoImage(app.tunaDown))

def drawStartPage(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
    image=ImageTk.PhotoImage(app.titleScreen))

def drawInstructions(app, canvas):
    canvas.create_image(app.width/2, app.height/2, 
    image=ImageTk.PhotoImage(app.instructionsPage))

def drawStatus(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'pink')
    fish1 = app.fishList[0]
    fish2 = app.fishList[1]
    fish3 = app.fishList[2]
    canvas.create_text(app.width//2, app.height/40, text=fish1.name, 
                        fill='black')
    canvas.create_text(app.width//2, app.height/3, text=fish2.name, 
                        fill='black')
    canvas.create_text(app.width//2, 2*app.height/3, text=fish3.name, 
                        fill='black')
    canvas.create_text(app.width//2, app.height/40 + 70, 
                        text=f'Health: {fish1.health}/10', fill='purple')
    canvas.create_text(app.width//2, app.height/3 + 70, 
                        text=f'Health: {fish2.health}/10', fill='purple')
    canvas.create_text(app.width//2, 2*app.height/3 + 70, 
                        text=f'Health: {fish3.health}/10', fill='purple')
    if fish1.species == 'anchovy':
        canvas.create_image(app.width//2, app.height/40 + 30, 
        image=ImageTk.PhotoImage(app.anchovyInit))
    if fish1.species == 'carp':
        canvas.create_image(app.width//2, app.height/40 + 30, 
        image=ImageTk.PhotoImage(app.carpInit))
    if fish1.species == 'rainbow':
        canvas.create_image(app.width//2, app.height/40 + 30, 
        image=ImageTk.PhotoImage(app.rainbowInit))
    if fish1.species == 'sturgeon':
        canvas.create_image(app.width//2, app.height/40 + 30, 
        image=ImageTk.PhotoImage(app.sturgeonInit))
    if fish1.species == 'tuna':
        canvas.create_image(app.width//2, app.height/40 + 30, 
        image=ImageTk.PhotoImage(app.tunaInit))
    if fish2.species == 'anchovy':
        canvas.create_image(app.width//2, app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.anchovyInit))
    if fish2.species == 'carp':
        canvas.create_image(app.width//2, app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.carpInit))
    if fish2.species == 'rainbow':
        canvas.create_image(app.width//2, app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.rainbowInit))
    if fish2.species == 'sturgeon':
        canvas.create_image(app.width//2, app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.sturgeonInit))
    if fish2.species == 'tuna':
        canvas.create_image(app.width//2, app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.tunaInit))
    if fish3.species == 'anchovy':
        canvas.create_image(app.width//2, 2*app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.anchovyInit))
    if fish3.species == 'carp':
        canvas.create_image(app.width//2, 2*app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.carpInit))
    if fish3.species == 'rainbow':
        canvas.create_image(app.width//2, 2*app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.rainbowInit))
    if fish3.species == 'sturgeon':
        canvas.create_image(app.width//2, 2*app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.sturgeonInit))
    if fish3.species == 'tuna':
        canvas.create_image(app.width//2, 2*app.height/3 + 30, 
        image=ImageTk.PhotoImage(app.tunaInit))

def redrawAll(app, canvas): 
    if app.startPage:
        drawStartPage(app, canvas)
    if app.instructions:
        drawInstructions(app, canvas)
    if app.playing:
        drawWater(app, canvas)
        drawSand(app, canvas)
        drawDragon(app, canvas)
        drawCoral(app, canvas)
        drawKelp(app, canvas)
        drawSeaweed(app, canvas)
        drawFish(app, canvas)
        if app.eating:
            drawFood(app, canvas, app.foodLocation[0], app.foodLocation[1])
            drawFish(app, canvas)
        if app.statuses:
            drawStatus(app, canvas)

runApp(width=600, height=400)