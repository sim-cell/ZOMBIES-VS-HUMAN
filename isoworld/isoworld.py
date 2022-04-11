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
from tkinter import W
from playsound import playsound



import pygame
from pygame.locals import *

###

versionTag = "2022"

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: simulation
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# all values are for initialisation. May change during runtime.

#numbers of elements
nbTrees = 15 #350
nbAgents = 40
nbDetails = 15

#environmental changes (nature)
DAY=True
WEATHER=True #True=sunny False=storm

#probs for humans and zombies
MAXAGEH=30
MAXAGEZ=20
PSHOOT=0.75
PROB_REPROD = 0.045
MAXHUNGER=30

#probs for foods
PROBDROPFOOD=0.3
DROPDAYFOOD=9
DECOMPDAYFOOD=15
NBFOOD=0
MAXFOOD= 30


#probs for gun
PROBDROPGUN=0.2
DROPDAYGUN=9
NBGUN=0
MAXGUN= 20

#probs for Cure
PROBDROPCURE=1.0
DROPDAYCURE=1
NBCURE=0
MAXCURE=20

#probs of environment
PROBTURN = 0.03    #randomly turn of road

#agent lists
guns = []
foods = []
zombies = []
humans = []
cure = []
lightning=[]

#occupied land by objects lists
clouds = []
occupied=[]  #occupied surface by objects




### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
###
### PARAMETERS: rendering
###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###




# display screen dimensions
screenWidth = 1400 # 930 #
screenHeight = 900 # 640 #

# world dimensions (ie. nb of cells in total)
worldWidth = 40#64
worldHeight = 40#64

# set surface of displayed tiles (ie. nb of cells that are rendered) -- must be superior to worldWidth and worldHeight
viewWidth = 40 #32
viewHeight = 40 #32

scaleMultiplier = 0.25 # re-scaling of loaded images = zoom

objectMapLevels = 10 # number of levels for the objectMap. This determines how many objects you can pile upon one another.

# set scope of displayed tiles
xViewOffset = 0
yViewOffset = 0


addNoise = False

maxFps = 30 # set up maximum number of frames-per-second

verbose = False # display message in console on/off
verboseFps = True # display FPS every once in a while

#max space to fill with objects
MAXENVOBJ = randint(2,worldWidth //10)
MAXSURFACE = (worldWidth * worldHeight*30)//100



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

#creating background images

night=pygame.image.load("assets/starsbig.png").convert_alpha()
day=pygame.image.load("assets/sunnydayy.png").convert_alpha()
cloudy=pygame.image.load("assets/cloudday.png").convert_alpha()


#creating clouds (the dimensions are different so do not use loadImage)
cloud = pygame.image.load('assets/cloud30.png').convert_alpha()
cloud = pygame.transform.scale(cloud, (int(100)*scaleMultiplier, int(100)*scaleMultiplier)) #setting the size

chargedcloud = pygame.image.load('assets/chargedcloud30.png').convert_alpha()
chargedcloud = pygame.transform.scale(chargedcloud, (int(100)*scaleMultiplier, int(100)*scaleMultiplier))

def loadImage(filename):
    global tileTotalWidthOriginal,tileTotalHeightOriginal,scaleMultiplier
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (int(tileTotalWidthOriginal*scaleMultiplier), int(tileTotalHeightOriginal*scaleMultiplier)))
    return image

#dloading all images
def loadAllImages():
    global tileType, objectType, agentType

    tileType = []
    objectType = []
    agentType = []


    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_27.png')) # grass
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_30.png')) # brick
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png')) # blue grass (?)
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png')) # grey brock
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_28.png'))  #for road
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_26.png')) #for water
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/VoxelTile_16.png')) #for sides of lake ---> to choise
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_22.png')) #
    tileType.append(loadImage('assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_31.png')) # ground
    tileType.append(loadImage('assets/ext/kenney_prototypepack/Isometric/floorGrass_S.png')) #floorGrass



    objectType.append(None) # default -- never drawn
    treeBig=loadImage('assets/basic111x128/tree.png') # normal tree
    treeBig = pygame.transform.scale(treeBig, (23, 70))
    #treeBig = pygame.transform.rotozoom(treeBig, 0, 1.2)
    objectType.append(treeBig)
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/VoxelTile_27.png')) # block
    objectType.append(loadImage('assets/basic111x128/tree_small_NW_ret_red.png')) # burning tree
    grassSmall=loadImage('assets/basic111x128/grass.png') #grass detail
    grassSmall = pygame.transform.scale(grassSmall, (25, 18))
    objectType.append(grassSmall)
    flowerSmall=loadImage('assets/ext/kenney_natureKit/Isometric/flower_red1_SE.png') # flower red
    flowerSmall = pygame.transform.scale(flowerSmall, (15, 20))
    objectType.append(flowerSmall)
    objectType.append(loadImage('assets/ext/kenney_natureKit/Isometric/canoe_NW.png')) #canoe
    objectType.append(loadImage('assets/ext/kenney_natureKit/Isometric/plant_bushDetailed_SW.png')) #plant detail

    #details for house
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Voxel tiles/VoxelTile_14.png')) #door
    objectType.append(loadImage('assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_23.png')) #window
    objectType.append(loadImage('assets/ext/kenney_prototypepack/Isometric/floorGrass_S.png')) #floorGrass
    objectType.append(loadImage('assets/ext/kenney_prototypepack/Isometric/stepsSmall_W.png')) #steps

    #clouds
    objectType.append(cloud) #normal cloud
    objectType.append(chargedcloud) #charged cloud

    #lightning
    lightningimage=loadImage('assets/basic111x128/lightning.png') #lightning
    lightningimage = pygame.transform.scale((lightningimage), (50, 50))
    objectType.append(lightningimage)

    #agent images
    agentType.append(None) # default -- never drawn
    agentType.append(loadImage('assets/basic111x128/vaccine.png')) # cure
    agentType.append(loadImage('assets/basic111x128/zomb.png')) # zombie
    agentType.append(loadImage('assets/basic111x128/man2.png')) # man
    agentType.append(loadImage('assets/basic111x128/combat.png')) #human wins
    agentType.append(loadImage('assets/basic111x128/bite.png')) #zombie wins
    agentType.append(loadImage('assets/basic111x128/woman.png')) # woman
    #agentType.append(loadImage('isoworld/assets/basic111x128/burger.png')) # burger
    agentType.append(loadImage('assets/basic111x128/food.png')) # foods
    gunSmall=loadImage('assets/basic111x128/gun.png') # gun
    gunSmall = pygame.transform.scale(gunSmall, (23, 15))
    agentType.append(gunSmall)
    agentType.append(loadImage('assets/basic111x128/babyBoy.png')) # babyBoy
    agentType.append(loadImage('assets/basic111x128/babyGirl.png')) # babyGirl
    agentType.append(loadImage('assets/basic111x128/man2Z.png')) # man
    agentType.append(loadImage('assets/basic111x128/womanZ.png')) # woman



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
grassDetId = 4
flowerRId = 5
canoeId = 6
plantDetId = 7
doorId = 8
windowId = 9
floorGrId = 10
stepsId = 11
cloudId = 12
chargedCloudId = 13
lightningId=14


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
#burgerId = 7
foodsId = 7
gunId = 8
babyBoyId = 9
babyGirlId = 10
manInfId = 11
womanInfId = 12

iconsH_list = [manId, winnerhumanId, womanId, babyGirlId, babyBoyId, womanInfId, manInfId]

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
    print ("=-=  Zombies vs Humans : A Classic War          =-=")
    print ("=-=                                             =-=")
    print ("=-=  BABANAZAROVA Dilyara                       =-=")
    print ("=-=  CELIK Simay                                =-=")
    print ("=-=  KUDRYAVTSEVA Kristina                      =-=")
    print ("=-=  original code by :                       =-=")
    print ("=-= nicolas.bredeche(at)sorbonne-universite.fr  =-=")
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
        #print("settingobject",x,y)
        objectMap[level][y][x] = type
    else:
        print ("[ERROR] setObjectMap(.) -- Cannot set object. Level does not exist.")
        return 0

def deleteObjectAt(x,y,level): # be sure not to have invalid values (no error checks)
    objectMap[level][y][x] = 0
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
        if getObjectAt(xNew,yNew) == 0 or getObjectAt(xNew,yNew) == 2: # dont move if collide with object (note that negative values means cell cannot be walked on)
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
        if random()<=0.8:
            self.gun=randint(1,10)
        else:
            self.gun=0
        self.infected = 0
        return

    def shoot(self):
        if random()<PSHOOT :
            if self.gun>0 :
                self.gun-=1
                return True
        return False


    def move3(self):
        PROB=0.6 #less than zombies to be able to get caught
        if not DAY:
            PROB=0.3 #during night they can't see
        if random()<PROB:
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
            elif random()<0.3: #not a high probability because if they always try to stay in the same case they will not move around
                self.move4()
            else:
                self.move() #they can ignore if there is an opposite sex near them and go in a random direction

        return

    #when a human sees another human they go towards them

    def move4(self):
        
        if self.type==manId:
            if getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y+worldHeight)%worldHeight ) == womanId: #x+1 y
                self.move2(1,0)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y+worldHeight)%worldHeight ) == womanId: #x-1 y
                self.move2(-1,0)
            elif getAgentAt((self.x+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == womanId: #x y+1
                self.move2(0,1)
            elif getAgentAt((self.x+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) == womanId: #x y-1
                self.move2(0,-1)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) == womanId: #x-1 y-1
                self.move2(-1,-1)
            elif getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y-1+worldHeight)%worldHeight ) ==womanId: #x+1 y-1
                self.move2(1,-1)
            elif getAgentAt((self.x+1+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == womanId: #x+1 y+1
                self.move2(1,1)
            elif getAgentAt((self.x-1+worldWidth)%worldWidth, (self.y+1+worldHeight)%worldHeight ) == womanId: #x-1 y+1
                self.move2(-1,1)
            else :
                self.move()
        elif self.type==womanId:
            maninneighbor=False
            for i in [0,1,-1]:
                for j in [0,1,-1]:
                    if not (i==0 and j==0): #not in the same case  
                        if getAgentAt((self.x+i+worldWidth)%worldWidth, (self.y+j+worldHeight)%worldHeight )==manId: #there is a man in neighbor
                            maninneigbor=True
            if not maninneighbor:
                self.move() #if there is no man then woman moves randomly if there is a man she does not move


        return


    def combat(self,zombies,met):
        success = self.shoot()
        for z in zombies:
            if (met(self,z)):
                print("combat")
                if success:
                    zombies.remove(z)
                    print("zombie got shot by ",id(self))
                    self.type=winnerhumanId
                else:
                    Tx=self.x
                    Ty=self.y
                    print("Human", id(self), "was infected and had gun :",self.gun)
                    self.infected += 1
                    if self.sex=='M':
                        self.type = manInfId
                        print("infected M")
                    else:
                        self.type = womanInfId
                        print("infected F")
                break
                   # print("will remove a Z now")
                    #zombies.append(Zombie(winnerzombieId,Tx,Ty))
                   # print("Z removed")

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
                        print("a baby is born ")
                        if sex_choice == ImageIdF:
                            list_humans.append(Female(sex_choice, coords[0], coords[1]))
                        else :
                            list_humans.append(Male(sex_choice, coords[0], coords[1]))
                    break
        return

    def eat(self, foods) : #when they eat food they become younger
        food=False
        for f in foods :
            if self.x== f.x and self.y==f.y :
                self.hunger+=f.energy
                self.age-=f.energy
                foods.remove(f)
                food=True
                print("human ate")
        if not food :
            self.hunger-=1

    def arming(self, guns) :
        for g in guns :
            if self.x== g.x and self.y==g.y :
                self.gun+=1
                print("armed")
                guns.remove(g)

    def takeCure(self, cure, manId, womanId):
        if self.infected >0:
            for i in cure:
                if self.x ==i.x and self.y==i.y :
                    self.infected = 0
                    if self.sex =='M':
                        self.type = manId
                        print("Female ", id(self), " cured")
                    else:
                        self.type = womanId
                        print("Male ", id(self), " cured")

                #cure.remove(i)
                break
        return

    def check_transition(h, zombies):
        if h.infected == 15:
            h.die()
            Tx=h.x
            Ty=h.y
            zombies.append(Zombie(zombieId,Tx,Ty))
        return

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


def met(agent1, agent2):
    exists=False
    if agent1.x==agent2.x and agent1.y==agent2.y:
        exists=True
    return exists


class RandDropAgents:

    def __init__(self):
        return

    def reset (self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldHeight()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)

    def getPosition(self):
        return (self.x,self.y)

    def getType(self):
        return self.type


class Cure(RandDropAgents):
    def __init__(self) :
        super().__init__()
        self.energy=0
        self.type = medicineId
        self.decomp=0
        self.reset()

    def randomDrop(list, it):
        for i in range(0,MAXCURE):
            list.append(Cure())
        return


class Food(RandDropAgents):
    def __init__(self) :
        super().__init__()
        self.energy=randint(2, 8)
        self.type = foodsId
        self.decomp=0
        self.reset()


    def decomposition(foods) :
        for f in foods :
            if f.decomp==DECOMPDAYFOOD :
                print("food decomposition")
                foods.remove(f)
            else :
                f.decomp+=1
        return

    def randomDrop(it,list):
        if (it != 0):
            if random() < PROBDROPFOOD:
                if it%DROPDAYFOOD==0 :
                    for i in range(0, randint(5, 10)):
                        if len(list)== MAXFOOD :
                            break
                        list.append(Food())
        return


class Gun(RandDropAgents) :
    def __init__(self) :
        super().__init__()
        self.type=gunId
        self.reset()

    def randomDrop(it,list):
        if (it != 0):
            if random() < PROBDROPGUN:
                if it%DROPDAYGUN == 0 :
                    for i in range(0,randint(5, 10)):
                        if len(list)== MAXGUN :
                            break
                        list.append(Gun())
        return


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### Initialise world
###
###

#create random environment


def cloudspawn():
    #creating the cloud matrix
    #interaction points are the corners and if they are touching every x iteration we hear lightning (maybe their color change)

    maxx=worldWidth/4
    maxy=worldHeight/4
    cx=randint(0,worldWidth)
    cy=randint(0,worldHeight)

    while len(clouds)<(worldHeight*worldWidth)//2:
        xx=randint(2,maxx)
        yy=randint(2,maxy)
        cx=randint(0,worldWidth)
        cy=randint(0,worldHeight)
        for x in range(0,xx):
            w=((x+cx)+worldWidth)%worldWidth
            for y in range(0,yy):
                l=((y+cy)+worldHeight)%worldHeight
                if random()<0.15:
                    setObjectAt(w,l,chargedCloudId,objectMapLevels-1)
                else :
                    setObjectAt(w,l,cloudId,objectMapLevels-1)
                clouds.append(1)




def createRoad(x,y,dir='x'):
    if dir== 'x' :
        for x2 in range(x, getWorldWidth()) :
            if getObjectAt(x2,y) != 0 or getTerrainAt(x2,y) != 0 or random()< PROBTURN:
                y1=((y-1+worldHeight)%worldHeight) #left
                y2=((y+1+worldHeight)%worldHeight) #right
                ychoix=choice([y1,y2]) #to continue with left or right
                dir='y'
                if getObjectAt(x2,ychoix) != 0 or getTerrainAt(x2,ychoix) != 0 :
                    #try the other side :
                    if ychoix == y1 :

                        ychoix= y2
                    else :
                        ychoix = y1
                    if getObjectAt(x2,ychoix) != 0 or getTerrainAt(x2,ychoix) != 0 :
                            break  #surrounded with the objects, finish the road
                return createRoad(((x2-1+worldWidth)%worldWidth),ychoix,dir)

            else :
                setTerrainAt(x2,y,4)#add a road
    if dir== 'y' :
        for y2 in range(y, getWorldHeight()) :
            if getObjectAt(x,y2) != 0 or getTerrainAt(x,y2) != 0 or random()< PROBTURN :
                x1=((x-1+worldWidth)%worldWidth) #left---->up
                x2=((x+1+worldWidth)%worldWidth) #right----->down
                xchoix=choice([x1,x2])
                dir='x'
                if getObjectAt(xchoix,y2) != 0 or getTerrainAt(xchoix,y2) != 0 :
                    #to try the other side :
                    if xchoix == x1 :
                        xchoix= x2
                    else :
                        xchoix = x1
                    if getObjectAt(xchoix,y2) != 0 or getTerrainAt(xchoix,y2) != 0 :
                            break  #surrounded with the objects, finish the road
                return createRoad(xchoix,((y2-1+worldHeight)%worldHeight),dir)
            else :
                setTerrainAt(x,y2,4) #add a road
    return

def addingTrees():
    for i in range(nbTrees):
        x = randint(0,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0 or getHeightAt(x,y) == 1:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,getWorldHeight()-1)
        setObjectAt(x,y,treeId,2)
        setObjectAt(x,y, -1,0)
    return


def createlake(x,y) :
    lakeTerrainMap =[
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 7, 5, 5, 5, 5, 0 ],
    [ 0, 7, 7, 7, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 7, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    ]

    lakeHeightMap = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, 0, -1, -1, -1, -1, 0 ],
    [ 0, 0, 0, 0, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, 0, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ]
    xforroad=0
    yforroad=0
    #putting the lake
    for w in range( len( lakeTerrainMap )):
        for l in range( len( lakeTerrainMap[0] )):
            xx=((x+w)+worldWidth)%worldWidth
            yy=((y+l)+worldHeight)%worldHeight
            if (w==len(lakeTerrainMap )//2 and l==0) :
                setTerrainAt(xx,yy,4)
                occupied.append((xx,yy))
                xforroad=xx
                yforroad=((yy-1)+worldHeight)%worldHeight
                continue
            occupied.append((xx,yy))
            setTerrainAt( xx, yy, lakeTerrainMap[w][l])
            setHeightAt( xx, yy, lakeHeightMap[w][l])
            """if you do this the agents can climb the objects
            setObjectAt( xx, yy, 0, -1)
            setObjectAt( xx, yy, 0, 0) """
            if (lakeHeightMap[w][l] == -1) :
                #this one prohibit agents from coming
                setObjectAt( xx, yy, -1, 0)

    createRoad(xforroad,yforroad,'x')
    #putting the canoe
    setObjectAt( ((x+6)+worldWidth)%worldWidth,((y+3)+worldHeight)%worldHeight, canoeId)
    return

def createHouse(x,y):

    #forbidden area around the house
    xforbidden=((x-1)+worldWidth)%worldWidth
    yborbidden1=((y-1)+worldHeight)%worldHeight
    yborbidden2=((y+7)+worldHeight)%worldHeight
    for i in range(0,7):
        w=((xforbidden+i)+worldWidth)%worldWidth
        setObjectAt(w,yborbidden1,-1,0)
        setObjectAt(w,yborbidden2,-1,0)
        occupied.append((w,yborbidden1))
        occupied.append((w,yborbidden2))
    for j in range(0,7):
            l=((y+j)+worldHeight)%worldHeight
            setObjectAt(xforbidden,l,-1,0)

    #putting the house
    for i in range(0,4):
        w=((x+i)+worldWidth)%worldWidth
        for j in range(0,7):
            l=((y+j)+worldHeight)%worldHeight
            for level in range(0,objectMapLevels-3):
                setObjectAt(w,l,blockId,level)
                #print(w,l)
            occupied.append((w,l))

    faceX=((x+4)+worldWidth)%worldWidth
    faceY1= ((y+2)+worldHeight)%worldHeight
    faceY2= ((y+4)+worldHeight)%worldHeight
    faceY3= ((y+6)+worldHeight)%worldHeight
    for c in [(faceX,y),(faceX,faceY1),(faceX,faceY2),(faceX,faceY3)]:
        occupied.append((c[0],c[1]))
        setObjectAt(c[0],c[1],-1,0)
        for level in range(0,objectMapLevels-3):
            setObjectAt(c[0],c[1],blockId,level)
    faceY4= ((y+1)+worldHeight)%worldHeight
    faceY5= ((y+5)+worldHeight)%worldHeight
    #adding windows
    for c in [(faceX,faceY4),(faceX,faceY5)]:
        occupied.append((c[0],c[1]))
        setObjectAt(c[0],c[1],-1,0)
        for level in range(0,objectMapLevels-3):
            if level == 4 :
                setObjectAt(c[0],c[1],windowId,level)
                continue
            setObjectAt(c[0],c[1],blockId,level)

    faceY6= ((y+3)+worldHeight)%worldHeight
    #adding the door
    for c in [(faceX,faceY6)]:
        occupied.append((c[0],c[1]))
        for level in range(3,objectMapLevels-3):
            setObjectAt(c[0],c[1],blockId,level)

    setObjectAt(faceX,faceY6,doorId,0)
    setObjectAt(faceX,faceY6,doorId,1)
    setObjectAt(faceX,faceY6,doorId,2)

    xforroad=((faceX+1)+worldWidth)%worldWidth
    createRoad(xforroad,faceY6)
    #adding flowers in front of the house
    faceX2=((faceX+1)+worldWidth)%worldWidth
    for c in [(faceX2,y),(faceX2,faceY4),(faceX2,faceY1),(faceX2,faceY2),(faceX2,faceY5),(faceX2,faceY3)] :
        occupied.append((c[0],c[1]))
        setTerrainAt( c[0], c[1], 8 )
        setObjectAt( c[0], c[1], flowerRId)
    return

def randEnv():
    nbobj=randint(2,MAXENVOBJ)
    i=nbobj
    while i>0 and len(occupied)<MAXSURFACE :
        type = 0
        if random()<0.3:
            type=1 #if 0 then house if 1 then lake
        nb=8 #tjrs pair
        x = randint(0,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while True and len(occupied)>0:
            nottrouve=True
            for (a,b) in occupied:
                if nottrouve :
                    if (x==a) and (y==b):
                        nottrouve=False
                        print("trouve x,y")
                        break
                    elif (((x+nb+worldWidth)%worldWidth)==a and ((y+nb+worldHeight)%worldHeight)==b) :
                        nottrouve=False
                        print("trouve x+,y+")
                        break
                    elif ((x==a) and ((y+nb+worldHeight)%worldHeight)==b) :
                        nottrouve=False
                        print("trouve x,y+")
                        break
                    elif (((x+nb+worldWidth)%worldWidth)==a and y==b) :
                        nottrouve=False
                        print("trouve x+,y")
                        break
                    elif (((x+nb/2+worldWidth)%worldWidth)==a and y==b):
                        nottrouve=False
                        print("trouve x/,y mil")
                        break
                    elif ((x==a) and ((y+nb/2+worldHeight)%worldHeight)):
                        nottrouve=False
                        print("trouve x,y/ mil")
                        break
                    elif (((x+nb/2+worldWidth)%worldWidth)==a and ((y+nb+worldHeight)%worldHeight)==b) :
                        nottrouve=False
                        print("trouve x/,y+ mil")
                        break
                    elif (((x+nb+worldWidth)%worldWidth)==a and ((y+nb/2+worldHeight)%worldHeight)==b) :
                        nottrouve=False
                        print("trouve x+,y/ mil")
                        break
                else :
                    break
            if (not  nottrouve) :
                x = randint(0,getWorldWidth()-1)
                y = randint(0,getWorldHeight()-1)
                continue
            else :
                break
        if type == 0 :
            createHouse(x,y)
            i-=1
        elif type == 1 :
            createlake(x,y)
            i-=1

    #adding details : flower, plant or grass
    for i in range(nbDetails):
        x = randint(0,getWorldWidth()-6)
        y = randint(0,20)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,20)
        setObjectAt(x,y,grassDetId)
    return

def fixEnv():

    #adding lake
    lakeTerrainMap =[
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 7, 5, 5, 5, 5, 0 ],
    [ 0, 7, 7, 7, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 7, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 5, 5, 5, 5, 5, 5, 5, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    ]

    lakeHeightMap = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, 0, -1, -1, -1, -1, 0 ],
    [ 0, 0, 0, 0, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, 0, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, -1, -1, -1, -1, -1, -1, -1, 0 ],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ]

    x_offset = 6
    y_offset = 20

    #putting the lake
    for x in range( len( lakeTerrainMap )):
        for y in range( len( lakeTerrainMap[0] )):
            setTerrainAt( x+x_offset, y+y_offset, lakeTerrainMap[x][y])
            setHeightAt( x+x_offset, y+y_offset, lakeHeightMap[x][y])

            #if you do this the agents can climb the objects
            setObjectAt( x+x_offset, y+y_offset, 0, -1)
            setObjectAt( x+x_offset, y+y_offset, 0, 0)
            if (lakeHeightMap[x][y] == -1) :
                #this one prohibit agents from coming
                setObjectAt( x+x_offset, y+y_offset, -1, 0)

    setObjectAt( 6+x_offset, 3+y_offset, canoeId)

    #-----------------------------------------------------------------------------------

    #adding details : flower, plant or grass
    for i in range(nbDetails):
        x = randint(0,getWorldWidth()-6)
        y = randint(0,20)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(0,getWorldWidth()-1)
            y = randint(0,20)
        setObjectAt(x,y,grassDetId)

    #-----------------------------------------------------------------------------------

    #adding house1
    for x in range(1,4):
        for y in range(13,20) :
            setObjectAt(x,y,-1,0)
            for level in range(1,objectMapLevels):
                setObjectAt(x,y,blockId,level)


    for c in [(4,13),(4,15),(4,17),(4,19)]:
        setObjectAt(c[0],c[1],-1,0)
        for level in range(1,objectMapLevels):
            setObjectAt(c[0],c[1],blockId,level)

    #adding windows
    for c in [(4,14),(4,18)]:
        setObjectAt(c[0],c[1],-1,0)
        for level in range(1,objectMapLevels):
            if level == 4 :
                setObjectAt(c[0],c[1],windowId,level)
                continue
            setObjectAt(c[0],c[1],blockId,level)

    #adding the door
    for c in [(4,16)]:
        for level in range(3,objectMapLevels):
            setObjectAt(c[0],c[1],blockId,level)
    #they can go through the door
    setObjectAt(4,16,doorId,1)
    setObjectAt(4,16,doorId,2)
    setObjectAt(4,16,doorId,3)

    for c in [(6,13),(6,14),(6,15),(6,17),(6,18),(6,19)] :
        setTerrainAt( c[0], c[1], 8 )
        setObjectAt( c[0], c[1], flowerRId,0)

    #-----------------------------------------------------------------------------------

    #adding house2
    for x in range(13,20):
        for y in range(1,4) :
            setObjectAt(x,y,-1,0)
            for level in range(1,objectMapLevels):
                setObjectAt(x,y,blockId,level)

    for c in [(13,4),(15,4),(17,4),(19,4)]:
        setObjectAt(c[0],c[1],-1,0)
        for level in range(1,objectMapLevels):
            setObjectAt(c[0],c[1],blockId,level)

    #adding windows
    for c in [(14,4),(18,4)]:
        setObjectAt(c[0],c[1],-1,0)
        for level in range(1,objectMapLevels):
            if level == 4 :
                setObjectAt(c[0],c[1],windowId,level)
                continue
            setObjectAt(c[0],c[1],blockId,level)

    #adding the door
    for c in [(16,4)]:
        for level in range(3,objectMapLevels):
            setObjectAt(c[0],c[1],blockId,level)
    setObjectAt(16,4,doorId,1)
    setObjectAt(16,4,doorId,2)
    setObjectAt(16,4,doorId,3)

    #adding floor grass around the house
    for c in [(12,5),(13,5),(14,5),(15,5),(17,5),(18,5),(19,5),(20,5)] :
        setObjectAt(c[0],c[1],floorGrId,0)
        if (c[0]==12 or c[0]==20) :
            for y in range (1,5):
                setObjectAt(c[0],y,floorGrId,0)

    #-----------------------------------------------------------------------------------

    #adding trees
    for i in range(nbTrees):
        x = randint(0,getWorldWidth()-7)
        y = randint(22,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0 or getHeightAt(x,y) == 1:
            x = randint(0,getWorldWidth()-7)
            y = randint(22,getWorldHeight()-1)
        setObjectAt(x,y,treeId,2)
        setObjectAt(x,y, -1,0)

    for i in range(nbTrees-10):
        x = randint(getWorldWidth()-5,getWorldWidth()-1)
        y = randint(0,getWorldHeight()-1)
        while getTerrainAt(x,y) != 0 or getObjectAt(x,y) != 0:
            x = randint(getWorldWidth()-5,getWorldWidth()-1)
            y = randint(0,getWorldHeight()-1)
        setObjectAt(x,y,treeId,2)
        setObjectAt(x,y,-1, 0)



    #-----------------------------------------------------------------------------------

    #adding a road
    for y in range(0,getWorldHeight()):
        setTerrainAt(getWorldWidth()-6, y, 4)
        setTerrainAt(getWorldWidth()-7 , y, 4)
        setObjectAt(getWorldWidth()-6 , y, 0)
        setObjectAt(getWorldWidth()-7 , y, 0)
        setObjectAt(getWorldWidth()-6 , y, -1, 2)
        setObjectAt(getWorldWidth()-7 , y, -1, 2)# add a virtual object: not displayed, but used to forbid agent(s) to come here.

    for x in range(4,getWorldWidth()-7):
        setTerrainAt(x, 16, 4)
        setObjectAt(x,16, 0)

    for y in range(4,16):
        setTerrainAt(16,y, 4)
        setObjectAt(16,y, 0)

    #-----------------------------------------------------------------------------------

     # adding pyramid-shape building
    building2TerrainMap = [
    [ 0, 1, 1, 1, 0 ],
    [ 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1 ],
    [ 1, 1, 1, 1, 1 ],
    [ 0, 1, 1, 1, 0 ]
    ]
    building2HeightMap = [
    [ 0, 1, 1, 1, 0 ],
    [ 1, 1, 2, 1, 1 ],
    [ 1, 2, 3, 2, 1 ],
    [ 1, 1, 2, 1, 1 ],
    [ 0, 1, 1, 1, 0 ]
    ]
    x_offset = getWorldWidth()-15
    y_offset = getWorldHeight()-6

    for x in range( len( building2TerrainMap[0]) ):
        for y in range( len( building2TerrainMap) ):
            setTerrainAt( x+x_offset, y+y_offset, building2TerrainMap[y][x] )
            setHeightAt( x+x_offset, y+y_offset, building2HeightMap[y][x] )
            setObjectAt( x+x_offset, y+y_offset, 0)
            setObjectAt( x+x_offset, y+y_offset, -1, 2) # add a virtual object: not displayed, but used to forbid objects to come here.

    return


def initWorld():
    global nbTrees, nbBurningTrees, zombies, humans, nbDetails

    cloudspawn()
    if getWorldWidth() >= 100 :
        fixEnv()
        randEnv()
        addingTrees()
    else :
        randEnv()
        addingTrees()

    #adding agents
    for i in range(nbAgents):
        zombies.append(Zombie(zombieId,-1,-1))
        if random()<0.5:
            humans.append(Male(manId))
        else:
            humans.append(Female(womanId))
        #ch = choice((m,f))
        #humans.append(ch)

    Cure.randomDrop(cure,it=1)

    return

### ### ### ### ###

def initAgents():
    return

### ### ### ### ###

def stepWorld( it = 0):

    for (x,y) in lightning:
        deleteObjectAt(x,y,objectMapLevels-2)
        lightning.remove((x,y))


    if it % (maxFps/10) == 0: #tour speed

        if WEATHER==False: #stormy
            for x in range(worldWidth):
                for y in range(worldHeight):
                    if getObjectAt(x,y,objectMapLevels-1) == chargedCloudId:
                        for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                            if getObjectAt((x+neighbours[0]+worldWidth)%worldWidth,(y+neighbours[1]+worldHeight)%worldHeight,objectMapLevels-1) == chargedCloudId:
                                if random()<0.03:
                                    lightning.append((x,y))
                                    setObjectAt(x,y,lightningId,objectMapLevels-2)
                                    #if random()<0.0012: #plays the sound of thunder but it is annoying
                                        #playsound('sounds/minithunder.wav')
                        if random()<0.005:
                            setObjectAt(x,y,cloudId,objectMapLevels-1)
                    elif getObjectAt(x,y,objectMapLevels-1) == cloudId:
                        for neighbours in ((-1,0),(+1,0),(0,-1),(0,+1)):
                            if getObjectAt((x+neighbours[0]+worldWidth)%worldWidth,(y+neighbours[1]+worldHeight)%worldHeight,objectMapLevels-1) == chargedCloudId:
                                if random()<0.3:
                                    setObjectAt(x,y,chargedCloudId,objectMapLevels-1)

        else:
            #if we want random clouds every once in a while
            if random()<0.1:
                for x in range(worldWidth):
                    for y in range(worldHeight):
                        if getObjectAt(x,y,objectMapLevels-1) == chargedCloudId or  getObjectAt(x,y,objectMapLevels-1) == cloudId:
                            deleteObjectAt(x,y,objectMapLevels-1)
                for i in clouds:
                    clouds.remove(i)

                cloudspawn()
            #if we reinitialize the clouds as mostly uncharged
            """
            if random()<0.1:
                for x in range(worldWidth):
                    for y in range(worldHeight):
                        if getObjectAt(x,y,objectMapLevels-1) == chargedCloudId :
                            if random()<0.2:
                                setObjectAt(x,y,cloudId,objectMapLevels-1)
                        elif getObjectAt(x,y,objectMapLevels-1) == cloudId :
                            if random()<0.05:
                                setObjectAt(x,y,chargedCloudId,objectMapLevels-1)"""
    return


### ### ### ### ###

def stepAgents(it = 0 ):
    # move agent
    if it % (maxFps/16) == 0: 
        print("stepped agents human count :",len(humans),"zombie count :",len(zombies))
        shuffle(foods)
        shuffle(zombies)
        shuffle(humans)
        Food.randomDrop(it, foods)
        Food.decomposition(foods)
        Gun.randomDrop(it, guns)

        for objList in [foods, guns, cure]:
            for i in objList:
                setAgentAt(i.x, i.y, i.type)
        for z in zombies:
            if z.type!=2:
                z.type=2   # shuffle agents in in-place (i.e. agents is modified)
            if z.decomp>MAXAGEZ:
                z.die()
                zombies.remove(z)
            elif z.dead==False:
                z.decomp+=1
                z.move3()
                z.direction=randint(0,3)
        for h in humans:
            if (h.type==winnerhumanId or h.type==babyBoyId or h.type==babyGirlId ): #if s/he won the combat
                if h.sex=='M':
                    h.type=manId
                else:
                    h.type=womanId

            if h.age>MAXAGEH or h.hunger==-1:
                h.die()
                
            h.check_transition(zombies)

            if h.dead:
                humans.remove(h)
            else:
                if h.infected != 0:
                    h.infected +=1
                    h.takeCure(cure, manId, womanId)
                else:
                    h.eat(foods)
                    h.arming(guns)
                    h.combat(zombies, met)
                    h.reproduire(humans, babyBoyId, babyGirlId, met)
                h.age+=1
                h.hunger-=1
                h.move3()

    return



### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### CORE: rendering
###
###


def render( it = 0, list_agents=iconsH_list):
    global xViewOffset, yViewOffset


    pygame.display.update()
    if DAY:
        if WEATHER:
            screen.blit(day,(0,0))
        else:
            screen.blit(cloudy,(0,0))


    else:
        screen.blit(night,(0,0))


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
                for iconId in list_agents:
                    if (getAgentAt(xTile, yTile)==iconId):
                        for h in humans:
                            if  h.dead==False and h.x==xTile and h.y==yTile : # agent on terrain?
                                screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))

                if ((getAgentAt( xTile, yTile ) == zombieId) or (getAgentAt( xTile, yTile ) == winnerzombieId)) :
                    for z in zombies:
                        if z.dead==False and z.x==xTile and z.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))

                if ((getAgentAt( xTile, yTile ) == foodsId)) :
                    for f in foods:
                        if f.x==xTile and f.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))

                if (getAgentAt( xTile, yTile ) == gunId) :
                    for f in guns:
                        if f.x==xTile and f.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))

                if (getAgentAt( xTile, yTile ) == medicineId) :
                    for f in cure:
                        if f.x==xTile and f.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))


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

    stepAgents(it)
    stepWorld(it)

    perdu = False
    winner = 0


    if (len(zombies)==0):
        print("all zombies are dead")
        perdu = True
        winner = 1 #1 if humans win(all zombies are dead), 2 if zombies win


    if (len(humans)==0):
        print("all humans are dead")
        perdu = True
        winner = 2


    if perdu == True :
        if winner == 1:
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

    if perdu == True :
        if winner == 2:
            print ("")
            print ("#### #### #### #### ####")
            print ("####                ####")
            print ("####     ZOMBIES WIN !    ####")
            print ("####                ####")
            print ("#### #### #### #### ####")
            print ("")
            print (">>> Score:",it,"--> BRAVO! ")
            print ("")
            pygame.quit()
            sys.exit()

    if it % 60 == 0:
        DAY=False
    if it % 120 == 0:
        DAY=True
        if random()<0.5 :
            WEATHER=True
        else:
            WEATHER=False


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