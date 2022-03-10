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
import math
import time
from playsound import playsound
  


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
nbTrees = 350 #350
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
worldWidth = 64#64
worldHeight = 64#64

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

    tileType.append(loadImage('isoworld/assets/basic111x128/plat.png')) # grass
    tileType.append(loadImage('isoworld/assets/ext/isometric-blocks/PNG/Platformer tiles/platformerTile_33.png')) # brick
    tileType.append(loadImage('isoworld/assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_12.png')) # blue grass (?)
    tileType.append(loadImage('isoworld/assets/ext/isometric-blocks/PNG/Abstract tiles/abstractTile_09.png')) # grey brock

    objectType.append(None) # default -- never drawn
    objectType.append(loadImage('isoworld/assets/basic111x128/tree_small_NW_ret.png')) # normal tree
    objectType.append(loadImage('isoworld/assets/basic111x128/blockHuge_N_ret.png')) # construction block
    objectType.append(loadImage('isoworld/assets/basic111x128/tree_small_NW_ret_red.png')) # burning tree
    #agent images
    agentType.append(None) # default -- never drawn
    agentType.append(loadImage('isoworld/assets/basic111x128/vaccine.png')) # medicine
    agentType.append(loadImage('isoworld/assets/basic111x128/zomb.png')) # zombie
    agentType.append(loadImage('isoworld/assets/basic111x128/human.png')) # human
    agentType.append(loadImage('isoworld/assets/basic111x128/combat.png')) #human wins
    agentType.append(loadImage('isoworld/assets/basic111x128/bite.png')) #zombie wins

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
grassId = 0
treeId = 1
burningTreeId = 3
medicineId = 1
zombieId = 2
winnerzombieId= 5
humanId = 3
winnerhumanId = 4
blockId = 2


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
class Human:
#,age,dead,hunger,gun
    def __init__(self,imageId, newx=-1, newy=-1):
        self.type = imageId
        self.age=0
        self.dead=False
        self.hunger=MAXHUNGER
        if random()<0.5:
            self.gun=randint(1,10)
        else:
            self.gun=0
        if newx<0:
            self.reset()
        else :
            self.x=newx
            self.y=newy
            setAgentAt(self.x,self.y,self.type)
        #self.reset()
        return

    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

    def getPosition(self):
        return (self.x,self.y)

    def die(self):
        self.dead=True

    
    def shoot(self):
        if random()<PSHOOT :
            if self.gun>0 :
                self.gun-=1
                return True
        return False 

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
        

    def getType(self):
        return self.type

    def combat(self,zombies,humans, foods):
        exists=False
        for z in zombies:
            if self.x==z.x and self.y==z.y:
                exists=True
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
                    break
        if not exists:
            self.age+=1
            self.hunger-=1
            self.move3()
    #return

    def reproduire(self, list_humans, imageID):
        if random()<PROB_REPROD:
            coords = self.getPosition()
            z = Human(imageID, coords[0], coords[1])
            list_humans.append(z)

                    

    def getPosition(self):
        return (self.x,self.y)
                

class Zombie:

    def __init__(self,imageId,newx,newy):
        self.decomp=0
        self.dead=False
        self.direction=randint(0,3) 
        self.type = imageId
        if newx<0:
            self.reset()
        else :
            self.x=newx
            self.y=newy
            setAgentAt(self.x,self.y,self.type)
        return

    def init(self, imageId, x, y):
        self.decomp=0
        self.dead=False
        self.direction=randint(0,3) 
        self.type = imageId
        self.x=x
        self.y=y
        
        return



		


    def reset(self):
        self.x = randint(0,getWorldWidth()-1)
        self.y = randint(0,getWorldWidth()-1)
        while getTerrainAt(self.x,self.y) != 0 or getObjectAt(self.x,self.y) != 0 or getAgentAt(self.x,self.y) != 0:
            self.x = randint(0,getWorldWidth()-1)
            self.y = randint(0,getWorldHeight()-1)
        setAgentAt(self.x,self.y,self.type)
        return

    def die(self): #from a headshot or from decomposition
        self.dead=True

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

    def move3(self):
        if random()<0.8:
            if self.direction==0:
                if getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+worldHeight)%worldHeight) == humanId :
                    self.move2(1,0)
                elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == humanId :
                    self.move2(1,1)  
                elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == humanId :
                    self.move2(1,-1)
                else :
                    self.move()
            elif self.direction==2:
                if getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+worldHeight)%worldHeight) == humanId :
                    self.move2(-1,0)
                elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == humanId :
                    self.move2(-1,1)  
                elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == humanId :
                    self.move2(-1,-1)
                else :
                    self.move()
            elif self.direction==1:
                if getAgentAt((self.x+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == humanId :
                    self.move2(0,1)
                elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == humanId :
                    self.move2(1,1)  
                elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y+1+worldHeight)%worldHeight) == humanId :
                    self.move2(1,1)
                else :
                    self.move()
            elif self.direction==3:
                if getAgentAt((self.x+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == humanId :
                    self.move2(0,-1)
                elif getAgentAt((self.x+1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == humanId :
                    self.move2(1,-1)  
                elif getAgentAt((self.x-1+worldWidth)%worldWidth,(self.y-1+worldHeight)%worldHeight) == humanId :
                    self.move2(-1,-1)
                else :
                    self.move()
        return

    def getType(self):
        return self.type

PROBDROP=0.3
PROBENERGY=0.5
DROPDAY=9
DECOMPDAY=15
NBFOODS=10


class Food:

    def __init__(self,imageId):
        self.type = imageId
        if random()<PROBEN :
            self.energy=5
        else :
            self.energy=2
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
        if (it%DROPDAY==0) :
            for i in range(NBFOODS):
                foods.append(Food(foodId))  #DISPLAY KALDI, decomp arttirmak, while it'na koy
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

def rendEnv():
	pass

def initWorld():
    global nbTrees, nbBurningTrees, zombies, humans, agents

    # add a pyramid-shape building
    #type of object
    building1TerrainMap = [
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
    for x in range( len( building1TerrainMap[0] ) ):
        for y in range( len( building1TerrainMap ) ):
            setTerrainAt( x+x_offset, y+y_offset, building1TerrainMap[x][y] )
            setHeightAt( x+x_offset, y+y_offset, building1HeightMap[x][y] )
            setObjectAt( x+x_offset, y+y_offset, -1 ) # add a virtual object: not displayed, but used to forbid agent(s) to come here.

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
    setObjectAt( x_offset+3, y_offset+4, treeId )
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
    for i in range(nbAgents):
        zombies.append(Zombie(zombieId,-1,-1))
        humans.append(Human(humanId))


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
    if it % (maxFps/60) == 0: #tour speed
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
MAXAGE=30
def stepAgents(humanID, it = 0 ):
    # move agent
    if it % (maxFps/10) == 0:
        shuffle(zombies)
        shuffle(humans)
        for z in zombies:
            if z.type!=2:
                z.type=2   # shuffle agents in in-place (i.e. agents is modified)
            if z.decomp>MAXAGE:
                z.die()
                zombies.remove(z)
            elif z.dead==False:
                z.decomp+=1
                z.move3()
	

        for h in humans:
            if h.type!=3:
                h.type=3 
            if h.age>MAXAGE:
                h.die()
                humans.remove(h)
            elif h.hunger==-1:
                h.die()
                humans.remove(h)
            elif h.dead==False:
                h.combat(zombies,humans,foods)
                h.reproduire(humans, humanID)
           # elif h.dead==False :
           #     
#return

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

            for level in range(objectMapLevels):
                if getObjectAt( xTile , yTile , level)  > 0: # object on terrain?
                    screen.blit( objectType[ getObjectAt( xTile , yTile, level) ] , (xScreen, yScreen - heightMultiplier*(level+1) ))
            if (getAgentAt( xTile, yTile ) != 0) :
                if (getAgentAt( xTile, yTile ) == humanId) :
                    for h in humans:
                        if  h.dead==False and h.x==xTile and h.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                elif (getAgentAt( xTile, yTile ) == zombieId) :
                    for z in zombies:
                        if z.dead==False and z.x==xTile and z.y==yTile : # agent on terrain?
                            screen.blit( agentType[ getAgentAt( xTile, yTile ) ] , (xScreen, yScreen - heightMultiplier ))
                else :
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

#player = BasicAgent(medicineId)
setAgentAt( mx+1, my+1, medicineId )

print ("initWorld:",datetime.datetime.now().timestamp()-timestamp,"second(s)")
timeStampStart = timeStamp = datetime.datetime.now().timestamp()

it = itStamp = 0

userExit = False

stepWorld(it)

while userExit == False:

    ID = humanId
    if it != 0 and it % 100 == 0 and verboseFps:
        print ("[fps] ", ( it - itStamp ) / ( datetime.datetime.now().timestamp()-timeStamp ) )
        timeStamp = datetime.datetime.now().timestamp()
        itStamp = it

    #screen.blit(pygame.font.render(str(currentFps), True, (255,255,255)), (screenWidth-100, screenHeight-50))

    render(it)
    
    stepAgents(ID, it)
    stepWorld(it)

    perdu = False


    if (len(zombies)==0):
        perdu = True 

    for h in humans:
        #if h.getPosition() == player.getPosition():
        if h.getPosition() == (mx,my):
            perdu = True
            playsound('isoworld/sounds/VOXScrm_Wilhelm scream (ID 0477)_BSB.wav')
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
        humans.append(Human(humanId))
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
