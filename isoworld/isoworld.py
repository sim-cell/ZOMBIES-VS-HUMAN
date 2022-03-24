
#
# World of Isotiles
# Author: nicolas.bredeche(at)sorbonne-universite.fr
#
# Started: 2018-11-17
# purpose: basic code developped for teaching artificial life and ecological simulation at Sorbonne Univ. (SU)
# course: L2, 2i013 Projet, "Vie Artificielle"
# licence: CC-BY-SA
#
# Requirements: Python3, Pygame
#
# Credits for third party resources used in this project:
# - Assets: https://www.kenney.nl/ (great assets by Kenney Vleugels with *public domain license*)
# - https://www.uihere.com/free-cliparts/space-medicines-extreme-2-video-game-arcade-game-8-bit-space-medicines-3996521
#
# Random bookmarks:
# - scaling images: https://stackoverflow.com/questions/43196126/how-do-you-scale-a-design-resolution-to-other-resolutions-with-pygame
# - thoughts on grid worlds: http://www-cs-students.stanford.edu/~amitp/game-programming/grids/
# - key pressed? https://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
# - basic example to display tiles: https://stackoverflow.com/questions/20629885/how-to-render-an-isometric-tile-based-world-in-python
# - pygame key codes: https://www.pygame.org/docs/ref/key.html
# - pygame capture key combination: https://stackoverflow.com/questions/24923078/python-keydown-combinations-ctrl-key-or-shift-key
# - methods to initialize a 2D array: https://stackoverflow.com/questions/2397141/how-to-initialize-a-two-dimensional-array-in-python
# - bug with SysFont - cf. https://www.reddit.com/r/pygame/comments/1fhq6d/pygamefontsysfont_causes_my_script_to_freeze_why/
#       myfont = pygame.font.SysFont(pygame.font.get_default_font(), 16)
#       myText = myfont.render("Hello, World", True, (0, 128, 0))
#       screen.blit(myText, (screenWidth/2 - text.get_width() / 2, screenHeight/2 - text.get_height() / 2))
#       ... will fail.
#
# TODO list
# - double buffer
# -.multiple agents


import sys
import datetime
from random import *
#import random
import math
import time
#from playsound import playsound
  


import pygame
from pygame.locals import *

###

versionTag = "2018-12-24_15h06"

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: simulation
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# all values are for initialisation. May change during runtime.

#numbers of elements
nbTrees = 30 #350
nbBurningTrees = 0 #15
nbAgents = 30

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: rendering
###x
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# display screen dimensions
screenWidth =  930 # 1400
screenHeight = 640 #900

# world dimensions (ie. nb of cells in total)
worldWidth = 32#64
worldHeight = 32#64

# set surface of displayed tiles (ie. nb of cells that are rendered) -- must be superior to worldWidth and worldHeight
viewWidth = 32 #32
viewHeight = 32 #32

scaleMultiplier = 0.25 # re-scaling of loaded images = zoom

objectMapLevels = 8 # number of levels for the objectMap. This determines how many objects you can pile upon one another.

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0

addNoise = False

maxFps = 30 # set up maximum number of frames-per-second

verbose = False # display message in console on/off
verboseFps = True # display FPS every once in a while

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### setting up Pygame/SDL
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

pygame.init()
#pygame.key.set_repeat(5,5)
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight), DOUBLEBUF)
pygame.display.set_caption('Zombieland')

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### CORE/USER: Image management
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def loadImage(filename):
    global tileTotalWidthOriginal,tileTotalHeightOriginal,scaleMultiplier
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image
#downloading all images
def loadAllImages():
    global tileType, objectType, agentType

    tileType = []
    objectType = []
    agentType = []

    tileType.append(loadImage('assets/basic111x128/plat.png')) # grasss
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_33.png')) # brick
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png')) # blue grass (?)
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png')) # grey brock

    objectType.append(None) # default -- never drawn
    objectType.append(loadImage('assets/basic111x128/tree_small_NW_ret.png')) # normal tree
    objectType.append(loadImage('assets/basic111x128/blockHuge_N_ret.png')) # construction block
    objectType.append(loadImage('assets/basic111x128/tree_small_NW_ret_red.png')) # burning tree
    #agent images
    agentType.append(None) # default -- never drawn
    agentType.append(loadImage('assets/basic111x128/vaccine.png')) # medicine
    agentType.append(loadImage('assets/basic111x128/zomb.png')) # zombie
    agentType.append(loadImage('assets/basic111x128/man.png')) # man
    agentType.append(loadImage('assets/basic111x128/combat.png')) #human wins
    agentType.append(loadImage('assets/basic111x128/bite.png')) #zombie wins
    agentType.append(loadImage('assets/basic111x128/woman.png')) # woman
    agentType.append(loadImage('assets/basic111x128/burger.png')) # burger
    agentType.append(loadImage('assets/basic111x128/foods.png')) # foods
    

def resetImages():
    global tileTotalWidth, tileTotalHeight, tileTotalWidthOriginal, tileTotalHeightOriginal, scaleMultiplier, heightMultiplier, tileVisibleHeight
    tileTotalWidth = tileTotalWidthOriginal * scaleMultiplier  # width of tile image, as stored in memory
    tileTotalHeight = tileTotalHeightOriginal * scaleMultiplier # height of tile image, as stored in memory
    tileVisibleHeight = tileVisibleHeightOriginal * scaleMultiplier # height "visible" part of the image, as stored in memory
    heightMultiplier = tileTotalHeight/2 # should be less than (or equal to) tileTotalHeight
    loadAllImages()
    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### CORE: objects parameters
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# spritesheet-specific -- as stored on the disk ==> !!! here, assume 128x111 with 64 pixels upper-surface !!!
# Values will be updated *after* image loading and *before* display starts
tileTotalWidthOriginal = 111  # width of tile image
tileTotalHeightOriginal = 128 # height of tile image
tileVisibleHeightOriginal = 64 # height "visible" part of the image, i.e. top part without subterranean part

###

tileType = []
objectType = []
agentType = []
#ID
noObjectId = noAgentId = 0
#objects
grassId = 0
treeId = 1
blockId = 2
burningTreeId = 3
#agents
medicineId = 1
zombieId = 2
# ---HUMAN-ICONS---
# the icon depends on Male/Female human
#humanId = 3
manId = 3
winnerhumanId = 4
winnerzombieId= 5
womanId = 6
burgerId = 7
foodsId =8

###

# re-scale reference image size -- must be done *after* loading sprites
resetImages()

###

terrainMap = [x[:] for x in [[0] * worldWidth] * worldHeight]
heightMap  = [x[:] for x in [[0] * worldWidth] * worldHeight]
objectMap = [ [ [ 0 for i in range(worldWidth) ] for j in range(worldHeight) ] for k in range(objectMapLevels) ]
agentMap   = [x[:] for x in [[0] * worldWidth] * worldHeight]

###

# set initial position for display on screen
xScreenOffset = screenWidth/2 - tileTotalWidth/2
yScreenOffset = 3*tileTotalHeight # border. Could be 0.

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CORE: get/set methods
###
###

def displayWelcomeMessage():

    print ("")
    print ("=-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-=")
    print ("=-=  World of Isotiles                          =-=")
    print ("=-=                                             =-=")
    print ("=-=  nicolas.bredeche(at)sorbonne-universite.fr =-=")
    print ("=-=  licence CC:BY:SA                           =-=")
    print ("=-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-= =-=")
    print (">> v.",versionTag)
    print ("")

    print ("Screen resolution : (",screenWidth,",",screenHeight,")")
    print ("World surface     : (",worldWidth,",",worldHeight,")")
    print ("View surface      : (",viewWidth,",",viewHeight,")")
    print ("Verbose all       :",verbose)
    print ("Verbose fps       :",verboseFps)
    print ("Maximum fps       :",maxFps)
    print ("")

    print ("# Hotkeys:")
    print ("\tcursor keys : move around (use shift for tile-by-tile move)")
    print ("\tv           : verbose mode")
    print ("\tf           : display frames-per-second")
    print ("\to           : decrease view surface")
    print ("\tO           : increase view surface")
    print ("\ts           : decrease scaling")
    print ("\tS           : increase scaling")
    print ("\tESC         : quit")
    print ("")

    return


def getWorldWidth():
    return worldWidth

def getWorldHeight():
    return worldHeight

def getViewWidth():
    return viewWidth

def getViewHeight():
    return viewHeight

def getTerrainAt(x,y):
    return terrainMap[y][x]
#changing the type
def setTerrainAt(x,y,type):
    terrainMap[y][x] = type

def getHeightAt(x,y):
    return heightMap[y][x]

def setHeightAt(x,y,height):
    heightMap[y][x] = height

def getObjectAt(x,y,level=0):
    if level < objectMapLevels:
        return objectMap[level][y][x]
    else:
        print ("[ERROR] getObjectMap(.) -- Cannot return object. Level does not exist.")
        return 0

def setObjectAt(x,y,type,level=0): # negative values are possible: invisible but tangible objects (ie. no display, collision)
    if level < objectMapLevels:
        objectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def getAgentAt(x,y):
    return agentMap[y][x]

def setAgentAt(x,y,type):
    agentMap[y][x] = type


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Agents
###
###
PSHOOT=0.5
PROB_REPROD = 0.03
MAXHUNGER=20

class BasicAgent:
    def __init__(self,imageId, newx, newy):
        self.type = imageId
        self.dead=False
        if newx<0:
            self.reset()
        else :
            self.x=newx
            self.y=newy
            setAgentAt(self.x,self.y,self.type)
        return

    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return
    
    def setHumanAt(self,x,y):
        self.x = x
        self.y = y
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

    def die(self): 
        self.dead=True

    def getType(self):
        return self.type

    def getPosition(self):
        return (self.x,self.y)
    def move(self):
        xNew = self.x
        yNew = self.y
        if random() < 0.5:
            xNew = ( self.x + [-1,+1][randint(0,1)] + getWorldWidth() ) % getWorldWidth()
        else:
            yNew = ( self.y + [-1,+1][randint(0,1)] + getWorldHeight() ) % getWorldHeight()
        if getObjectAt(xNew,yNew) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        elif getObjectAt(xNew,yNew) == 2: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt(self.x,self.y,noAgentId)
            self.x = xNew
            self.y = yNew
            setAgentAt(self.x,self.y,self.type)
        
        if verbose == True:
            print ("agent of type ",str(self.type),"located at (",self.x,",",self.y,")")
        return


    def move2(self,xNew,yNew):
        success = False
        if getObjectAt( (self.x+xNew+worldWidth)%worldWidth , (self.y+yNew+worldHeight)%worldHeight ) == 0: # dont move if collide with object (note that negative values means cell cannot be walked on)
            setAgentAt( self.x, self.y, noAgentId)
            self.x = ( self.x + xNew + worldWidth ) % worldWidth
            self.y = ( self.y + yNew + worldHeight ) % worldHeight
            setAgentAt( self.x, self.y, self.type)
            success = True
        if verbose == True:
            if success == False:
                print ("agent of type ",str(self.type)," cannot move.")
            else:
                print ("agent of type ",str(self.type)," moved to (",self.x,",",self.y,")")
        return
    def move3():
        return


class Human(BasicAgent):
#,age,dead,hunger,gun
    def __init__(self,imageId, newx=-1, newy=-1):
        super().__init__(imageId, newx, newy)
        self.age=0
        self.sex=None
        self.hunger=MAXHUNGER
        if random()<0.5:
            self.gun=randint(1,10)
        else:
            self.gun=0
        return

    def shoot(self):
        if random()<PSHOOT :
            if self.gun>0 :
                self.gun-=1
                return True
        return False 


    def move3(self):
        if random()<0.5:
            if getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y+worldHeight)%worldHeight ) == zombieId: #x+1 y
                self.move2(-1,0)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y+worldHeight)%worldHeight ) == zombieId: #x-1 y
                self.move2(1,0)
            elif getAgentAt((self.x+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == zombieId: #x y+1
                self.move2(0,-1)
            elif getAgentAt((self.x+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) == zombieId: #x y-1
                self.move2(0,1)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) == zombieId: #x-1 y-1
                self.move2(1,1)
            elif getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) == zombieId: #x+1 y-1
                self.move2(-1,1)
            elif getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == zombieId: #x+1 y+1
                self.move2(-1,-1)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == zombieId: #x-1 y+1
                self.move2(1,-1)
            else :
                self.move()
        return


    def combat(self,zombies,humans,foods,met):
        for z in zombies:
            if (met(self,z)):
                if self.shoot()==True:
                    zombies.remove(z)
                    self.type=4
                    self.age+=1
                    self.hunger-=1
                    self.move3()
                else:
                    Tx=self.x
                    Ty=self.y
                    humans.remove(self)
                    zombies.append(Zombie(winnerzombieId,Tx,Ty))
                    return
        self.age+=1
        self.hunger-=1
        self.move3()
        return

   # def reproduire(self, list_humans, imageIdF, imageIdM, met):
    def reproduire(self, list_humans, ImageIdM, ImageIdF, met):
        options=[ImageIdF, ImageIdM]
        sex_choice = choice(options)
        for h in list_humans:
            if (met(self, h)):
                if self.getType()!=h.getType():#self.instanceOf(Male)&&h.instanceOf(Female) || self.instanceOf(Female)&&h.instanceOf(Male):
                    if random()<PROB_REPROD:
                        coords = self.getPosition()
                        z=Male(sex, coords[0], coords[1])
                        if sex_choice == imageIdF:
                            z = Female(sex, coords[0], coords[1])
                        list_humans.append(z)
                    break
        return

    def eat(self, foods) :
        food=False
        for f in foods :
            if self.x== f.x and self.y==f.y :
                self.hunger+=f.energy
                foods.remove(f)
                food=True
        if not food:
            self.hunger-=1

          
class Male(Human):
    def __init__(self,imageId, newx=-1, newy=-1):
        super().__init__(imageId, newx=-1, newy=-1)
        self.sex='M'
class Female(Human):
    def __init__(self,imageId, newx=-1, newy=-1):
        super().__init__(imageId, newx=-1, newy=-1)
        self.sex='F'

 

class Zombie(BasicAgent):

    def __init__(self,imageId,newx,newy):
        super().__init__(imageId, newx, newy)
        self.decomp=0
        self.direction=randint(0,3) 
        return


    def move3(self):
        if random()<0.8:
            for agentId in [manId, womanId]:
                if self.direction==0:
                    if getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+worldHeight)%worldHeight) == agentId :
                        self.move2(1,0)
                        return
                    elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == agentId :
                        self.move2(1,1)
                        return
                    elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == agentId :
                        self.move2(1,-1)
                        return
                elif self.direction==2:
                    if getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+worldHeight)%worldHeight) == agentId :
                        self.move2(-1,0)
                        return
                    elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == agentId :
                        self.move2(-1,1)
                        return
                    elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == agentId :
                        self.move2(-1,-1)
                        return
                elif self.direction==1:
                    if getAgentAt((self.x+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == agentId :
                        self.move2(0,1)
                        return
                    elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == agentId :
                        self.move2(1,1)
                        return
                    elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == agentId :
                        self.move2(1,1)
                        return
                elif self.direction==3:
                    if getAgentAt((self.x+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == agentId :
                        self.move2(0,-1)
                        return
                    elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == agentId :
                        self.move2(1,-1)
                        return
                    elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == agentId :
                        self.move2(-1,-1)
                        return
        self.move()
        return



PROBDROP=0.3
PROBENERGY=0.5
DROPDAY=9
DECOMPDAY=15
NBFOODS=10
MAXFOOD= 20


class Food:

    def __init__(self):
        if random()<PROBENERGY :
            self.energy=5
            self.type = burgerId
        else :
            self.energy=2
            self.type = foodsId
        self.decomp=0
        self.reset()
        return

    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return
    
    

    def randomDrop(it,foods):
        if (it%DROPDAY==0 and len(foods)<MAXFOOD) :
            for i in range(NBFOODS):
                foods.append(Food())  #DISPLAY KALDI, decomp arttirmak, while it'na koy
        return 

    def decomposition(foods) :
        for f in foods :
            if f.decomp==DECOMPDAY :
                foods.remove(f)
            else :
                f.decomp+=1
        return

    def getPosition(self):
        return (self.x,self.y)

    def getType(self):
        return self.type


foods = []
zombies = []
humans = []


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Initialise world
###
###
mx = 3
my = 3
MAXMOUNT = (int)(worldHeight/10)
"""def randEnv():
    for ind in range(0,randint(0,MAXMOUNT+1)):
        wid=randint(0,10)
        len=randint(0,10)
        terrainMap=[[]]
        for i in range(wid) :

            terrainMap[i] = [3 for j in range(len)]

        heightMap=[[]]
        for w in range(wid):
            for l in range(len):
                heightMap[w][l]=randint(1,3)
        x_offset = randint(0,32)
        y_offset = randint(0,32)
        for x in range(wid):
            for y in range(len):
                setTerrainAt( x+x_offset, y+y_offset, terrainMap[x][y] )
                setHeightAt( x+x_offset, y+y_offset, heightMap[x][y] )
                setObjectAt( x+x_offset, y+y_offset, 0)
    return"""



def initWorld():
    global nbTrees, nbBurningTrees, zombies, humans, agents

    # add a pyramid-shape building
    #type of object
    #randEnv()
    """building1TerrainMap = [
    [ 2, 2, 2, 2 ],
    [ 2, 3, 3, 2 ],
    [ 2, 3, 3, 2 ],
    [ 2, 2, 2, 2 ]
    ]
    #height of building
    building1HeightMap = [
    [ 1, 1, 1, 1 ],
    [ 1, 0, 0, 1 ],
    [ 1, 0, 0, 1 ],
    [ 1, 0, 0, 1 ]
    ]
    #place of building
    x_offset = mx
    y_offset = my
   
    #putting the building 
    for x in range( len( building1TerrainMap[0] )):
        for y in range( len( building1TerrainMap )):
            setTerrainAt( x+x_offset, y+y_offset, building1TerrainMap[x][y] )
            setHeightAt( x+x_offset, y+y_offset, building1HeightMap[x][y] )
            setObjectAt( x+x_offset, y+y_offset, 0) # add a virtual object: not displayed, but used to forbid agent(s) to come here.
    # add another pyramid-shape building with a tree on top
    building2TerrainMap = [
    [ 0, 2, 2, 2, 2, 2, 0 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 2, 2, 2, 2, 2, 2, 2 ],
    [ 0, 2, 2, 2, 2, 2, 0 ]
    ]
    building2HeightMap = [
    [ 0, 1, 1, 1, 1, 1, 0 ],
    [ 1, 1, 1, 1, 1, 1, 1 ],
    [ 1, 2, 2, 2, 2, 2, 1 ],
    [ 1, 2, 3, 3, 3, 2, 1 ],
    [ 1, 2, 3, 4, 3, 2, 1 ],
    [ 1, 2, 3, 3, 3, 2, 1 ],
    [ 1, 2, 2, 2, 2, 2, 1 ],
    [ 1, 1, 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 1, 1, 0 ]
    ]
    x_offset = 4
    y_offset = 13
    for x in range( len( building2TerrainMap[0] ) ):
        for y in range( len( building2TerrainMap ) ):
            setTerrainAt( x+x_offset, y+y_offset, building2TerrainMap[y][x] )
            setHeightAt( x+x_offset, y+y_offset, building2HeightMap[y][x] )
            setObjectAt( x+x_offset, y+y_offset, -1 ) # add a virtual object: not displayed, but used to forbid agent(s) to come here.
    setObjectAt( x_offset+3, y_offset+4, treeId )"""
    #orange thing collumn
    for c in [(20,2),(30,2),(30,12),(20,12)]:
        for level in range(0,objectMapLevels):
            setObjectAt(c[0],c[1],blockId,level)
            #koprusu
    for i in range(9): 
        setObjectAt(21+i,2,blockId,objectMapLevels-1)
        setObjectAt(21+i,12,blockId,objectMapLevels-1)
        setObjectAt(20,3+i,blockId,objectMapLevels-1)
        setObjectAt(30,3+i,blockId,objectMapLevels-1)
    #adding agents
    m = Male(manId)
    f = Female(womanId)
    for i in range(nbAgents):
        zombies.append(Zombie(zombieId,-1,-1))
        if random()<0.5:
            humans.append(f)
        else:
            humans.append(m)
        #ch = choice((m,f))
        #humans.append(ch)




    #adding trees
    for i in range(nbTrees):
        x = randint(0,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,getWorldHeight()-1)
        setObjectAt(x,y,treeId)
    #adding burning trees
    for i in range(nbBurningTrees):
        x = randint(0,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,getWorldHeight()-1)
        setObjectAt(x,y,burningTreeId)

    return

### ### ### ### ###

def initAgents():
    return

### ### ### ### ###

def stepWorld( it = 0 ):
    if it % (maxFps/180) == 0: #tour speed
        for x in range(worldWidth):
            for y in range(worldHeight):
                #burning the trees
                if getObjectAt(x,y) == treeId:
                    for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                        if getObjectAt((x+neighbours[0]+worldWidth)%worldWidth,(y+neighbours[1]+worldHeight)%worldHeight) == burningTreeId:
                            setObjectAt(x,y,burningTreeId)
                        elif getAgentAt((x+neighbours[0]+worldWidth)%worldWidth,(y+neighbours[1]+worldHeight)%worldHeight) == zombieId:
                            setObjectAt(x,y,burningTreeId)
    return
### ### ### ### ###

def met(agent1, agent2):
    exists=False
    if agent1.x==agent2.x and agent1.y==agent2.y:
        exists=True
    return exists

### ### ### ### ###
MAXAGE=30
def stepAgents(maleID,womanId, it = 0 ):
    # move agent
    if it % (maxFps/10) == 0:
        shuffle(foods)
        shuffle(zombies)
        shuffle(humans)
        Food.randomDrop(it, foods)
        for z in zombies:
            if z.type!=2:
                z.type=2   # shuffle agents in in-place (i.e. agents is modified)
            if z.decomp>MAXAGE:
                z.die()
                zombies.remove(z)
            elif z.dead==False:
                z.decomp+=1
                z.move3()
                z.direction=randint(0,3)
        for h in humans:
            if not (h.type==3 or h.type==6):
                if h.sex=='M':
                    h.type=3
                else:
                    h.type=6
            #    h.type=3
            if h.age>MAXAGE:
                h.die()
                humans.remove(h)
            elif h.hunger==-1:
                h.die()
                humans.remove(h)

            elif h.dead==False:

                h.combat(zombies,humans,foods, met)
                h.reproduire(humans, manId, womanId, met)

    return


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CORE: rendering
###
###

def render( it = 0 ):
    global xViewOffset, yViewOffset

    pygame.draw.rect(screen, (0,0,0), (0, 0, screenWidth, screenHeight), 0) # overkill - can be optimized. (most sprites are already "naturally" overwritten)
    #pygame.display.update()

    for y in range(getViewHeight()):
        for x in range(getViewWidth()):
            # assume: north-is-upper-right

            xTile = ( xViewOffset + x + getWorldWidth() ) % getWorldWidth()
            yTile = ( yViewOffset + y + getWorldHeight() ) % getWorldHeight()

            heightNoise = 0
            if addNoise == True: # add sinusoidal noise on height positions
                if it%int(math.pi*2*199) < int(math.pi*199):
                    # v1.
                    heightNoise = math.sin(it/23+yTile) * math.sin(it/7+xTile) * heightMultiplier/10 + math.cos(it/17+yTile+xTile) * math.cos(it/31+yTile) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise
                else:
                    # v2.
                    heightNoise = math.sin(it/13+yTile*19) * math.cos(it/17+xTile*41) * heightMultiplier
                    heightNoise = math.sin(it/199) * heightNoise

            height = getHeightAt( xTile , yTile ) * heightMultiplier + heightNoise

            xScreen = xScreenOffset + x * tileTotalWidth / 2 - y * tileTotalWidth / 2
            yScreen = yScreenOffset + y * tileVisibleHeight / 2 + x * tileVisibleHeight / 2 - height

            screen.blit( tileType[ getTerrainAt( xTile , yTile ) ] , (xScreen, yScreen)) # display terrain

            #for i in humans:
            #    print(i)

            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( objectType[ getObjectAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))
            if (getAgentAt( xTile, yTile ) != 0) :
                if ((getAgentAt( xTile, yTile ) == manId) or (getAgentAt( xTile, yTile ) == womanId)) :
                    for h in humans:
                        if  h.dead==False and h.x==xTile and h.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                
                if (getAgentAt( xTile, yTile ) == zombieId) :
                    for z in zombies:
                        if z.dead==False and z.x==xTile and z.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                if ((getAgentAt( xTile, yTile ) == burgerId) or (getAgentAt( xTile, yTile ) == foodsId)) :
                    for f in foods:
                        if f.x==xTile and f.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                """else :
                     screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))"""

    return

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### MAIN
###
###

timestamp = datetime.datetime.now().timestamp()

loadAllImages()

displayWelcomeMessage()

initWorld()
initAgents()

#player = BasicAgent(medicineId)
setAgentAt( mx+1, my+1, medicineId )

print ("initWorld:",datetime.datetime.now().timestamp()-timestamp,"second(s)")
timeStampStart = timeStamp = datetime.datetime.now().timestamp()

it = itStamp = 0

userExit = False

stepWorld(it)

while userExit == False:

    if it != 0 and it % 100 == 0 and verboseFps:
        print ("[fps] ", ( it - itStamp ) / ( datetime.datetime.now().timestamp()-timeStamp ) )
        timeStamp = datetime.datetime.now().timestamp()
        itStamp = it

    #screen.blit(pygame.font.render(str(currentFps), True, (255,255,255)), (screenWidth-100, screenHeight-50))

    render(it)
    
    stepAgents(manId, womanId, it)
    stepWorld(it)

    perdu = False


    if (len(zombies)==0):
        perdu = True 

    for h in humans:
        #if h.getPosition() == player.getPosition():
        if h.getPosition() == (mx,my):
            perdu = True
            #playsound('isoworld/sounds/VOXScrm_Wilhelm scream (ID 0477)_BSB.wav')
            break

    if perdu == True:
        print ("")
        print ("#### #### #### #### ####")
        print ("####                ####")
        print ("####     HUMANS WIN !    ####")
        print ("####                ####")
        print ("#### #### #### #### ####")
        print ("")
        print (">>> Score:",it,"--> BRAVO! ")
        print ("")
        pygame.quit()
        sys.exit()

    if it % 10 == 0:
        m = Male(manId)
        f = Female(womanId)
        if random()<0.5:
            humans.append(m)
        else:
            humans.append(f)
        #ch = choice((m,f))
        #humans.append(ch)
        zombies.append(Zombie(zombieId,-1,-1))

    # continuous stroke
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        xViewOffset  = (xViewOffset - 1 + getWorldWidth() ) % getWorldWidth()
        if verbose:
            print("View at (",xViewOffset ,",",yViewOffset,")")
    elif keys[pygame.K_RIGHT] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        xViewOffset = (xViewOffset + 1 ) % getWorldWidth()
        if verbose:
            print("View at (",xViewOffset ,",",yViewOffset,")")
    elif keys[pygame.K_DOWN] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        yViewOffset = (yViewOffset + 1 ) % getWorldHeight()
        if verbose:
            print("View at (",xViewOffset,",",yViewOffset,")")
    elif keys[pygame.K_UP] and not ( keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] ):
        yViewOffset = (yViewOffset - 1 + getWorldHeight() ) % getWorldHeight()
        if verbose:
            print("View at (",xViewOffset,",",yViewOffset,")")

    # single stroke
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                userExit = True
            elif event.key == pygame.K_j:
                player.move2(0,+1);
            elif event.key == pygame.K_u:
                player.move2(0,-1);
            elif event.key == pygame.K_k:
                player.move2(+1,0);
            elif event.key == pygame.K_h:
                player.move2(-1,0);
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                addNoise = not(addNoise)
                print ("noise is",addNoise) # easter-egg
            elif event.key == pygame.K_v:
                verbose = not(verbose)
                print ("verbose is",verbose)
            elif event.key == pygame.K_f:
                verboseFps = not(verboseFps)
                print ("verbose FPS is",verboseFps)
            elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                xViewOffset  = (xViewOffset - 1 + getWorldWidth() ) % getWorldWidth()
                if verbose:
                    print("View at (",xViewOffset ,",",yViewOffset,")")
            elif event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                xViewOffset = (xViewOffset + 1 ) % getWorldWidth()
                if verbose:
                    print("View at (",xViewOffset ,",",yViewOffset,")")
            elif event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                yViewOffset = (yViewOffset + 1 ) % getWorldHeight()
                if verbose:
                    print("View at (",xViewOffset,",",yViewOffset,")")
            elif event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                yViewOffset = (yViewOffset - 1 + getWorldHeight() ) % getWorldHeight()
                if verbose:
                    print("View at (",xViewOffset,",",yViewOffset,")")
            elif event.key == pygame.K_o and not( pygame.key.get_mods() & pygame.KMOD_SHIFT ) :
                if viewWidth > 1:
                    viewWidth = int(viewWidth / 2)
                    viewHeight = int(viewHeight / 2)
                    print (viewWidth)
                if verbose:
                    print ("View surface is (",viewWidth,",",viewHeight,")")
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if viewWidth < worldWidth :
                    viewWidth = viewWidth * 2
                    viewHeight = viewHeight * 2
                if verbose:
                    print ("View surface is (",viewWidth,",",viewHeight,")")
            elif event.key == pygame.K_s and not( pygame.key.get_mods() & pygame.KMOD_SHIFT ) :
                if scaleMultiplier > 0.125:
                    scaleMultiplier = scaleMultiplier / 2
                if scaleMultiplier < 0.125:
                    scaleMultiplier = 0.125
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if scaleMultiplier < 1.0:
                    scaleMultiplier = scaleMultiplier * 2
                if scaleMultiplier > 1.0:
                    scaleMultiplier = 1.0
                resetImages()
                if verbose:
                    print ("scaleMultiplier is ",scaleMultiplier)

    pygame.display.flip()
    fpsClock.tick(maxFps) # recommended: 30 fps

    it += 1

fps = it / ( datetime.datetime.now().timestamp()-timeStampStart )
print ("[Quit] (", fps,"frames per second )")

pygame.quit()
sys.exit()
