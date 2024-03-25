""" simpleGE.py 

    3.0 edition
    
    high-level tools to simplify pygame programming
    for Game Programming - The L-Line
    by Andy Harris, 2006
    
    3.0 modifications Spring 2024
    
    refactored Sprite class to combine BasicSprite and SuperSprite
    Sprite now combines behavior of old BasicSprite and SuperSprite    
    Added Spritesheet class for character animation and tile extraction
    changed show() method of GUI elements to not require position
    Gave GUI elements (esp labels) alpha by default
    added makeColorRect() option to Sprites for easier prototyping
    SpriteGroups are still supported, but not essential
    Rationalized event-checking: update, checkEvents, doEvents
    Scene, sprite, and UI elements all have a process() method.
    Scene also has processEvent(event)
    older scene methods still supported but deprecated
    Add size as optional parameter in Scene constructor    

"""

import pygame, math, time
pygame.init()
pygame.mixer.init()

class Scene(object):
    """ encapsulates the IDEA / ALTER framework
        properties:
        sprites - a list of sprite objects
            that forms the primary sprite group
        background - the background surface
        screen - the display screen
        
        it's generally best to add all sprites 
        as attributes, so they can have access
        to each other if needed    
        
        default size is 640x480, but you can change in constructor
    """
    
    def __init__(self, size = (640, 480)):
        """ initialize the game engine
            set up a sample sprite for testing
        """
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        
        self.sampleSprite = SuperSprite(self)
        self.sampleSprite.setSpeed(3)
        self.sampleSprite.setAngle(0)
        self.sampleSprite.boundAction = self.sampleSprite.WRAP
        self.sprites = [self.sampleSprite]
        self.groups = []
    
    def start(self):
        """ sets up the sprite groups
            begins the main loop
        """
        self.mainSprites = pygame.sprite.OrderedUpdates(self.sprites)
        self.groups.append(self.mainSprites)
        
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        while self.keepGoing:
            self.__mainLoop()
        pygame.quit()
        
    def setImage(self, imageFile, autoSize = True):
        """ loads image to background.  By default, the image
            is resized to the screen size. You can pass 'False' as
            the second parameter to turn off this behavior. 
        """
        self.background = pygame.image.load(imageFile)
        if autoSize:
            newX = self.screen.get_size()[0]
            newY = self.screen.get_size()[1]
            self.background = pygame.transform.scale(self.background, (newX, newY))
            
    def stop(self):
        """stops the loop"""
        self.keepGoing = False
    
    def __mainLoop(self):
        """ manage all the main events 
            automatically called by start
        """
        self.clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keepGoing = False
            self.doEvents(event)
            self.processEvent(event)
        
        self.update()
        self.process()
        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
            group.draw(self.screen)
        
        pygame.display.flip()

    def makeSpriteGroup(self, sprites):
        """ create a group called groupName
            containing all the sprites in the sprites 
            list.  This group will be added after the 
            sprites group, and will automatically
            clear, update, and draw
            May not really be necessary as the spriteList
            can now contain lists of sprites
        """
        tempGroup = pygame.sprite.OrderedUpdates(sprites)
        return tempGroup
    
    def addGroup(self, group):
        """ adds a sprite group to the groups list for
            automatic processing 
        """
        self.groups.append(group)

    def doEvents(self, event):
        """ overwrite this method to add your own events.
            Works like normal event handling, passes event
            object
        """
        pass
        
    def processEvent(self, event):
        """
            doEvents, renamed for consistency 
        """
        pass
        
    def update(self):
        """ happens once per frame, after event parsing.
            Overwrite to add your own code, esp event handling
            that doesn't require event obj. (pygame.key.get_pressed, 
            pygame.mouse.get_pos, etc)
            Also a great place for collision detection
        """
        pass
    
    def process(self):
        """ just like update, but added for consistency with 
            sprite
        """
        pass
    
    def setCaption(self, title):
        """ set's the scene's title text """
        pygame.display.set_caption(title)
        
    def isKeyPressed(self, key):
        """ uses hardware polling to see if a certain key is pressed """
        keysDown = pygame.key.get_pressed()
        return keysDown[key]



class Sprite(pygame.sprite.Sprite):
  
    """ combines old basicSprite with superSprite
        heavy emphasis on properties 
        
    """
  
    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)

        self.scene = scene
        self.screen = scene.screen
        self.screenWidth = self.scene.background.get_width()
        self.screenHeight = self.scene.background.get_height()

        # image and rect defaults to 25x25 yellow square
        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        
        #position        
        self.x = 100
        self.y = 100
        
        #motion private attributes
        #initialize directly to get clean starting values
        self.__moveAngle = 0
        self.__imageAngle = 0
        self.__speed = 0
        self.__dx = 0 
        self.__dy = 0
        
        # motion properties
        self.dx = 0
        self.dy = 0
        self.speed = 0 
        self.moveAngle = 0
        self.oldCenter = self.position
        
        
        # visibility
        self.visible = True
        self.clicked = False
        self.mouseOver = False
        self.mouseDown = False
        
        # boundary constants
        self.WRAP = 0
        self.BOUNCE = 1
        self.STOP = 2
        self.HIDE = 3
        self.CONTINUE = 4
        
        self.boundAction = self.WRAP
        
    @property 
    def x(self):
        return self.__x
    
    @x.setter 
    def x(self, value):
        self.__x = value
        self.rect.centerx = self.__x

    @property 
    def y(self):
        return self.__y
    
    @y.setter 
    def y(self, value):
        self.__y = value
        self.rect.centery = self.__y
        
    # convenience position properties
    @property 
    def top(self):
        return self.rect.top
    
    @top.setter
    def top(self, top):
        self.rect.top = top
        self.y = self.rect.centery
        
    @property 
    def bottom(self):
        return self.rect.bottom
    
    @bottom.setter 
    def bottom(self, bottom):
        self.rect.bottom = bottom
        self.y = self.rect.centery
    
    @property 
    def left(self):
        return self.rect.left 
    
    @left.setter 
    def left(self, left):
        self.rect.left = left
        self.x = self.rect.centerx

    @property 
    def right(self):
        return self.rect.right 
    
    @right.setter 
    def right(self, right):
        self.rect.right = right
        self.x = self.rect.centerx
        
    @property 
    def position(self):
        return ((self.x, self.y))
    
    @position.setter 
    def position(self, position):
        self.x = position[0]
        self.y = position[1]
        self.oldCenter = self.position

    @property 
    def dx(self):
        return self.__dx
    
    @dx.setter 
    def dx(self, value):
        self.__dx = value
        #self.speedAngleFromVector()        

    @property 
    def dy(self):
        return self.__dy
    
    @dy.setter 
    def dy(self, value):
        self.__dy = value
        #self.speedAngleFromVector()        

    @property 
    def speed(self):
        # calculates speed based on dx and dy
        return self.__speed

    @speed.setter 
    def speed(self, speed):
        # calculates dx and dy along with moveAngle
        self.__speed = speed
        self.vectorFromSpeedAngle()

    @property 
    def moveAngle(self):
        return self.__moveAngle        
        
    @moveAngle.setter 
    def moveAngle(self, moveAngle):
        self.__moveAngle = moveAngle
        self.vectorFromSpeedAngle()
        
    @property 
    def imageAngle(self):
        return self.__imageAngle
    
    @imageAngle.setter 
    def imageAngle(self, imageAngle):
        #put rotation code here
        self.__imageAngle = imageAngle
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.imageMaster, self.__imageAngle)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
  
    def setAngle(self, angle):
        self.moveAngle = angle
        self.imageAngle = angle
        
    def turnBy(self, angle):
        self.moveAngle += angle
        self.imageAngle += angle
  
    def copyImage(self, imageSurface):
        """ copies a surface as a new image. mainly used in 
            animation 
        """
        self.image = imageSurface
        self.imageMaster = self.image 
        self.imageAngle = self.__imageAngle
        
    def vectorFromSpeedAngle(self):
        #calculates dx and dy from speed and angle
        
        theta = self.__moveAngle / 180.0 * math.pi
        self.normalDX = math.cos(theta)
        self.normalDY = math.sin(theta)
        self.dx = self.normalDX * self.speed
        self.dy = self.normalDY * -self.speed
        
        #print(f"{self.dx=}, {self.dy=}")
        
    def speedAngleFromVector(self):
        self.__speed = math.sqrt((self.__dx * self.__dx) + (self.__dy * self.__dy))
        
        dy = self.dy * -1
        dx = self.dx
        
        radians = math.atan2(dy, dx)
        self.__moveAngle = radians / math.pi * 180      
        
    def forward(self, distance):
        # moves distance pixels in the current image angle
        theta = self.imageAngle / 180.0 * math.pi
        dx = math.cos(theta) * distance
        dy = math.sin(theta) * distance
        dy *= -1        

        self.x += dx
        self.y += dy        
        
    def addForce(self, amt, angle):
        """ apply amt of thrust in angle.
            change speed and dir accordingly
            add a force straight down to simulate gravity
            in rotation direction to simulate spacecraft thrust
            in dir direction to accelerate forward
            at an angle for retro-rockets, etc.
        """

        #calculate dx dy based on angle
        radians = angle * math.pi / 180
        ddx = amt * math.cos(radians)
        ddy = amt * math.sin(radians) * -1
        
        self.dx += ddx
        self.dy += ddy
        
    def checkClicked(self):
        self.clicked = False
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouseOver = True
        else:
            self.mouseOver = False

        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.mouseOver:
                self.mouseDown = True

        #check for mouse release
        if self.mouseDown:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.mouseDown = False
                if self.mouseOver:
                    self.clicked = True
    
    def update(self):
        #self.vectorFromSpeedAngle()
        self.x += self.dx
        self.y += self.dy
        self.checkBounds()
        self.rect.center = (self.x, self.y)
        self.checkClicked()
        self.process()
        
    def setBoundAction(self, action):
        self.boundAction = action
        
    def checkBounds(self):

        """ checks boundary and acts based on 
            self.BoundAction.
            WRAP: wrap around screen (default)
            BOUNCE: bounce off screen
            STOP: stop at edge of screen
            HIDE: move off stage and wait
            CONTINUE: keep going at present course and speed
            
            automatically called by update()
            
            over-write for your own collision behavior
        """
        
        # ignore boundaries if we are hidden
        if self.visible:
            scrWidth = self.screen.get_width()
            scrHeight = self.screen.get_height()
            
            #create variables to simplify checking
            offRight = offLeft = offTop = offBottom = offScreen = False
            
            if self.x > scrWidth:
                offRight = True
            if self.x < 0:
                offLeft = True
            if self.y > scrHeight:
                offBottom = True
            if self.y < 0:
                offTop = True
                
            if offRight or offLeft or offTop or offBottom:
                offScreen = True
            
            if self.boundAction == self.WRAP:
                if offRight:
                    self.x = 0
                if offLeft:
                    self.x = scrWidth
                if offBottom:
                    self.y = 0
                if offTop:
                    self.y = scrHeight
            
            elif self.boundAction == self.BOUNCE:
                if offLeft or offRight:
                    self.dx *= -1
                if offTop or offBottom:
                    self.dy *= -1
                    
                #self.updateVector()
                #self.rotation = self.dir
            
            elif self.boundAction == self.STOP:
                if offScreen:
                    self.speed = 0
            
            elif self.boundAction == self.HIDE:
                if offScreen:
                    self.hide()
            
            elif self.boundAction == self.CONTINUE:
                pass
                
            else:
                # assume it's CONTINUE - keep going forever
                pass    
            
            
    def setSize(self, newX, newY):
        self.image = pygame.transform.scale(self.image, (newX, newY))
        self.imageMaster = self.image
        self.rect = self.image.get_rect()
        
    def setImage (self, imageFile):
        """ loads the given file name as the master image
            default setting should be facing east.  Image
            will be rotated automatically """
        self.image = pygame.image.load(imageFile)
        if imageFile.endswith(".png"):
          self.image = self.image.convert_alpha()
        else:
          self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.imageMaster = self.image
        

        
    def colorRect(self, color, size):
        """ sets image to a specific color and size
            useful for prototyping.  You can change
            transparency with sprite.image.set_alpha()
        """
    
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.imageMaster = self.image
        
    def collidesWith(self, target):
        """ boolean function. Returns True if the sprite
            is currently colliding with the target sprite,
            False otherwise
        """
        
        collision = False
        if self.visible:
            if target.visible:
                if self.rect.colliderect(target.rect):
                    collision = True
        return collision

    def process(self):
        #meant to be overwritten
        pass

    def hide(self):
        self.oldPosition = self.rect.center
        self.x = -1000
        self.y = -1000
        self.visible = False
        
    def show(self):
        self.visible = True
        self.x = self.oldPosition[0]
        self.y = self.oldPosition[1]
        
    def isKeyPressed(self, key):
        #convenience method
        return self.scene.isKeyPressed(key)    
    
    def distanceTo(self, point):
        """ returns distance to any point in pixels
            can be used in circular collision detection
        """
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        
        dist = math.sqrt((dx * dx) + (dy * dy))
        return dist
    
    def dirTo(self, point):
        """ returns direction (in degrees) to 
            a point """
        
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        dy *= -1
        
        radians = math.atan2(dy, dx)
        dir = radians * 180 / math.pi
        dir += 180
        return dir
    
    def drawTrace(self, color=(0x00, 0x00, 0x00)):
        """ traces a line between previous position
            and current position of object. Set sprite's 
            position property before turning on drawTrace
            for best performance.
        """
        pygame.draw.line(self.scene.background, color, self.oldCenter,
                         self.rect.center, 3)
        self.screen.blit(self.scene.background, (0, 0))
        self.oldCenter = self.position

class Label(pygame.sprite.Sprite):
    """ a basic label 
        properties: 
            font: font to use
            text: text to display
            fgColor: foreground color
            bgColor: background color (None for transparent bg)
            center: position of label's center
            size: (width, height) of label
            clearBack: if true, background is invisible
    """
    
    def __init__(self, fontName = "freesansbold.ttf"):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontName, 20)
        self.text = ""
        self.fgColor = ((0xFF, 0xFF, 0xFF))
        self.bgColor = ((0x00, 0x00, 0x00))
        self.center = (100, 100)
        self.size = (150, 30)
        self.clearBack = False
        
    def update(self):
        self.checkEvents()
        self.process()
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        
        if self.clearBack:
            fontSurface = self.font.render(self.text, True, self.fgColor)
            self.image.set_alpha(255)
        else:
            fontSurface = self.font.render(self.text, True, self.fgColor, self.bgColor)
            self.image.fill(self.bgColor)

        #center the text
        xPos = (self.image.get_width() - fontSurface.get_width())/2
        
        self.image.blit(fontSurface, (xPos, 5))
            
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
    def checkEvents(self):
        pass
    
    def process(self):
        pass
    
    def hide(self):
        self.oldPosition = self.center
        self.center = (-1000, -1000)
    
    def show(self):
        self.center = self.oldPosition

class Button(Label):
    """ a button based on the label 
        same properties as label +
        active: True if user is clicking on sprite
                False if user is not currently clicking
        clicked: True when user releases mouse over a 
                 currently active button
    """

    def __init__(self):
        Label.__init__(self)
        self.active = False
        self.clicked = False
        self.fgColor = (0x00, 0x00, 0x00)
        self.bgColor = (0xCC, 0xCC, 0xCC)
    
    def update(self):
        Label.update(self)
        
        self.clicked = False

        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True

        #check for mouse release
        if self.active == True:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.active = False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True

class TxtInput(Button):
    """ Simple text input 
        Click on input to get to edit mode
        will switch background to activeColor
        delete to clear box, backspace to back up
        text will be available as a property.
        Note readkeys needs an event object
        so it must be called from scene's 
        doEvents() method
    """
    
    def __init__(self):
        super().__init__()
        self.takingInput = False
        self.activeColor = pygame.Color("yellow")
        self.standardColor = self.bgColor
        
    def readKeys(self, event):
        
        if self.takingInput:
            self.bgColor = pygame.Color("yellow")
        else:
            self.bgColor = self.standardColor
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.takingInput = not self.takingInput
            else:
                self.takingInput = False

        if event.type == pygame.KEYDOWN:
            if self.takingInput:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_DELETE:
                    self.text = ""
                else:
                    self.text += event.unicode

class Scroller(Button):
    """ like a button, but has a numeric value that 
        can be decremented by clicking on left half
        and incremented by clicking on right half.
        new atributes:
            value: the scroller's numeric value
            minValue: minimum value
            maxValue: maximum value
            increment: How much is added or subtracted
            format: format of string interpolation
    """
    
    def __init__(self):
        Button.__init__(self)
        self.minValue = 0
        self.maxValue = 10
        self.increment = 1
        self.value = 5
        self.format = f"<<  {self.value}  >>"
        
    def update(self):
        Button.update(self)
        if self.active:
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < self.rect.centerx:
                self.value -= self.increment
                if self.value < self.minValue:
                    self.value = self.minValue
            else:
                self.value += self.increment
                if self.value > self.maxValue:
                    self.value = self.maxValue

        self.text = f"<< {self.value} >>"

class MultiLabel(pygame.sprite.Sprite):
    """ accepts a list of strings, creates a multi-line
        label to display text 
        same properties as label except textLines
        is a list of strings. There is no text
        property.
        Set the size manually. Vertical size should be at 
        least 30 pixels per line (with the default font)
    """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.textLines = ["This", "is", "sample", "text"]
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 100)
        self.clicked = False
        self.active = False
        
    def update(self):
        self.checkEvents()
        self.process()
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        numLines = len(self.textLines)
        vSize = self.image.get_height() / numLines
        
        for lineNum in range(numLines):
            currentLine = self.textLines[lineNum]
            fontSurface = self.font.render(currentLine, True, self.fgColor, self.bgColor)
            #center the text
            xPos = (self.image.get_width() - fontSurface.get_width())/2
            yPos = lineNum * vSize
            self.image.blit(fontSurface, (xPos, yPos + 15))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        
        self.clicked = False
        
        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True

        #check for mouse release
        if self.active == True:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.active = False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True

    def checkEvents(self):
        pass
    
    def process(self):
        pass
    
    def hide(self):
        self.oldCenter = self.center
        self.center = (-1000, -1000)
        
    def show(self):
        self.center = self.oldCenter
        
class Timer(object):
  def __init__(self):
    super().__init__()
    self.start()
    self.totalTime = 1000

  def start(self):
    self.__startTime = time.time()
    
  def getElapsedTime(self):
    self.__now = time.time()
    elapsedTime = self.__now - self.__startTime
    return elapsedTime

  def getTimeLeft(self):
    timeLeft = self.totalTime - self.getElapsedTime()
    return timeLeft

class Sound(object):
  def __init__(self, soundFile):
    super().__init__()
    self.sound = pygame.mixer.Sound(soundFile)

  def play(self):
    self.sound.play()

class SpriteSheet():
    """ handles basic character animation """
    
    def __init__(self, imageFile, cellSize, numRows, numCols, delay = .1):
        """ requires 
          * imageFile: master image file name
          * cellSize: size of one cell in pixels (width, height)
          * numRows: number of animation rows
          * numCols: number of animation columns
          * delay: gap (in seconds) between animation flips
          
          Note that the animation must be regular and rectangular
          (that is all rows have same number of columns, and all
           cells are the same size)
          Use the offset to indicate the upper-left corner of the
          animation rectangle you want to use
          You can use more than one animation object if you have
          different cell sizes or counts.
        """
        
        self.offset = (0, 0)
        self.imageFileName = imageFile
        self.cellSize = cellSize        
        self.NUMROWS = numRows
        self.NUMCOLS = numCols
        self.delay = delay
        self.animRow = 0
        self.animCol = 0
        self.timer = Timer()
        self.startCol = 0

        self.animImage = pygame.image.load(self.imageFileName)
        self.animImage.convert_alpha()
        
    def getCellImage(self, row, col):
        """ given a row and column, returns the appropriate sub-image """
        imgOut = pygame.Surface(self.cellSize, pygame.SRCALPHA)
        
        cellWidth = self.cellSize[0]
        cellHeight = self.cellSize[1]
        
        cellX = self.offset[0] + (row * cellWidth)
        cellY = self.offset[1] + (col * cellHeight)
        
        sourceRect = pygame.Rect(cellX, cellY, cellWidth, cellHeight)
        
        imgOut.blit(self.animImage, (0, 0), sourceRect)

        return(imgOut)

    def getNext(self, animRow):
        """ returns the next image in the current row """
        self.animRow = animRow
        if self.timer.getElapsedTime() > self.delay:
            self.timer.start()
            if self.animCol < self.NUMCOLS -1:
                self.animCol += 1
            else:
                self.animCol = self.startCol
        return (self.getCellImage(self.animCol, self.animRow))



class BasicSprite(pygame.sprite.Sprite):
    """ ***DEPRECATED - Please use simpleGE.Sprite instead ***
        use this sprite when you want to 
        directly control the sprite with dx and dy
        or want to extend in another direction than SuperSprite
    """
    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)

        self.scene = scene
        self.screen = scene.screen

        self.image = pygame.Surface((25, 25))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.visible = True

    @property 
    def x(self):
        return self.__x
    
    @x.setter 
    def x(self, value):
        self.__x = value
        self.rect.centerx = self.__x

    @property 
    def y(self):
        return self.__y
    
    @y.setter 
    def y(self, value):
        self.__y = value
        self.rect.centery = self.__y

    @property 
    def dx(self):
        return self.__dx
    
    @dx.setter 
    def dx(self, value):
        self.__dx = value

    @property 
    def dy(self):
        return self.__dy
    
    @dy.setter 
    def dy(self, value):
        self.__dy = value


    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.checkBounds()
        self.rect.center = (self.x, self.y)
        self.checkEvents()
        
    def checkBounds(self):
        scrWidth = self.screen.get_width()
        scrHeight = self.screen.get_height()
        if self.visible:
            if self.x > scrWidth:
                self.x = 0
            if self.x < 0:
                self.x = scrWidth
            if self.y > scrHeight:
                self.y = 0
            if self.y < 0:
                self.y = scrHeight
            
    def setSize(self, newX, newY):
        self.image = pygame.transform.scale(self.image, (newX, newY))
        self.rect = self.image.get_rect()
        
    def setImage (self, imageFile):
        """ loads the given file name as the master image
            default setting should be facing east.  Image
            will be rotated automatically """
        self.image = pygame.image.load(imageFile)
        if imageFile.endswith(".png"):
          self.image = self.image.convert_alpha()
        else:
          self.image = self.image.convert()
        self.rect = self.image.get_rect()
          
    def collidesWith(self, target):
        """ boolean function. Returns True if the sprite
            is currently colliding with the target sprite,
            False otherwise
        """
        collision = False
        if self.visible:
            if target.visible:
                if self.rect.colliderect(target.rect):
                    collision = True
        return collision

    def checkEvents(self):
        #meant to be overwritten
        pass

    def hide(self):
        self.oldPosition = self.rect.center
        self.x = -1000
        self.y = -1000
        self.visible = False
        
    def show(self):
        self.visible = True
        self.x = self.oldPosition[0]
        self.y = self.oldPosition[1]
        

class SuperSprite(pygame.sprite.Sprite):
    """ *** DEPRECATED - Please use simpleGE.Sprite instead ***
    
        An enhanced Sprite class
        expects a gameEngine.Scene class as its one parameter
        Use methods to change image, direction, speed
        Will automatically travel in direction and speed indicated
        Automatically rotates to point in indicated direction
        Five kinds of boundary collision
    """

    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen
        
        #create constants
        self.WRAP = 0
        self.BOUNCE = 1
        self.STOP = 2
        self.HIDE = 3
        self.CONTINUE = 4
        
        #create a default text image as a placeholder
        #This will usually be changed by a setImage call
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.imageMaster = self.font.render(">sprite>", True, (0, 0,0), (0xFF, 0xFF, 0xFF))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        
        #create properties
        #most will be changed through method calls
        self.x = 200
        self.y = 200
        self.dx = 0
        self.dy = 0
        self.dir = 0
        self.rotation = 0
        self.speed = 0
        self.maxSpeed = 10
        self.minSpeed = -3
        self.boundAction = self.WRAP
        self.pressed = False
        self.oldCenter = (100, 100)
        self.visible = True
    
    def update(self):
        self.oldCenter = self.rect.center
        self.checkEvents()
        self.__rotate()
        self.__calcVector()
        self.__calcPosition()
        self.checkBounds()
        self.rect.center = (self.x, self.y)
    
    def checkEvents(self):
        """ overwrite this method to add your own event code """
        pass

    def __rotate(self):
        """ PRIVATE METHOD
            change visual orientation based on 
            rotation property.
            automatically called in update.
            change rotation property directly or with 
            rotateBy(), setAngle() methods
        """
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.imageMaster, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
    
    def __calcVector(self):
        """ calculates dx and dy based on speed, dir
            automatically called in update() 
        """
        theta = self.dir / 180.0 * math.pi
        self.dx = math.cos(theta) * self.speed
        self.dy = math.sin(theta) * self.speed
        self.dy *= -1
    
    def __calcPosition(self):
        """ calculates the sprites position adding
            dx and dy to x and y.
            automatically called in update()
        """
        self.x += self.dx
        self.y += self.dy

    def checkBounds(self):
        """ checks boundary and acts based on 
            self.BoundAction.
            WRAP: wrap around screen (default)
            BOUNCE: bounce off screen
            STOP: stop at edge of screen
            HIDE: move off stage and wait
            CONTINUE: keep going at present course and speed
            
            automatically called by update()
        """
        
        # ignore boundaries if we are hidden
        if self.visible:
            scrWidth = self.screen.get_width()
            scrHeight = self.screen.get_height()
            
            #create variables to simplify checking
            offRight = offLeft = offTop = offBottom = offScreen = False
            
            if self.x > scrWidth:
                offRight = True
            if self.x < 0:
                offLeft = True
            if self.y > scrHeight:
                offBottom = True
            if self.y < 0:
                offTop = True
                
            if offRight or offLeft or offTop or offBottom:
                offScreen = True
            
            if self.boundAction == self.WRAP:
                if offRight:
                    self.x = 0
                if offLeft:
                    self.x = scrWidth
                if offBottom:
                    self.y = 0
                if offTop:
                    self.y = scrHeight
            
            elif self.boundAction == self.BOUNCE:
                if offLeft or offRight:
                    self.dx *= -1
                if offTop or offBottom:
                    self.dy *= -1
                    
                self.updateVector()
                #self.rotation = self.dir
            
            elif self.boundAction == self.STOP:
                if offScreen:
                    self.speed = 0
            
            elif self.boundAction == self.HIDE:
                if offScreen:
                    self.speed = 0
                    self.setPosition((-1000, -1000))
            
            elif self.boundAction == self.CONTINUE:
                pass
                
            else:
                # assume it's CONTINUE - keep going forever
                pass    
    
    def setSpeed(self, speed):
        """ immediately sets the objects speed to the 
            given value.
        """
        self.speed = speed

    def speedUp(self, amount):
        """ changes speed by the given amount
            Use a negative value to slow down
        """
        self.speed += amount
        if self.speed < self.minSpeed:
            self.speed = self.minSpeed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
    
    def setAngle(self, dir):
        """ sets both the direction of motion 
            and visual rotation to the given angle
            If you want to set one or the other, 
            set them directly. Angle measured in degrees
        """            
        self.dir = dir
        self.rotation = dir
    
    def turnBy (self, amt):
        """ turn by given number of degrees. Changes
            both motion and visual rotation. Positive is
            counter-clockwise, negative is clockwise 
        """
        self.dir += amt
        if self.dir > 360:
            self.dir = amt
        if self.dir < 0:
            self.dir = 360 - amt
        self.rotation = self.dir
    
    def rotateBy(self, amt):
        """ change visual orientation by given
            number of degrees. Does not change direction
            of travel. 
        """
        self.rotation += amt
        if self.rotation > 360:
            self.rotation = amt
        if self.rotation < 0:
            self.rotation = 360 - amt
            
    def setImageAngle(self, amt):
        """ convenience function for compatibility with simpleGame """
        self.rotation = amt
        
    def setMoveAngle(self, amt):
        """ convenience function for compatibility with simplegame """
        self.dir = amt
    
    def setImage (self, image):
        """ loads the given file name as the master image
            default setting should be facing east.  Image
            will be rotated automatically """
        self.imageMaster = pygame.image.load(image)
        if image.endswith(".png"):
          self.imageMaster = self.imageMaster.convert_alpha()
        else:
          self.imageMaster = self.imageMaster.convert()
    
    def setDX(self, dx):
        """ changes dx value and updates vector """
        self.dx = dx
        self.updateVector()
    
    def addDX(self, amt):
        """ adds amt to dx, updates vector """
        self.dx += amt
        self.updateVector()
        
    def setDY(self, dy):
        """ changes dy value and updates vector """
        self.dy = dy
        self.updateVector()

    def addDY(self, amt):
        """ adds amt to dy and updates vector """
        self.dy += amt
        self.updateVector()
    
    def setComponents(self, components):
        """ expects (dx, dy) for components
            change speed and angle according to dx, dy values """
            
        (self.dx, self.dy) = components
        self.updateVector()
        
    def setBoundAction (self, action):
        """ sets action for boundary.  Values are
            self.WRAP (wrap around edge - default)
            self.BOUNCE (bounce off screen changing direction)
            self.STOP (stop at edge of screen)
            self.HIDE (move off-stage and stop)
            self.CONTINUE (move on forever)
            Any other value allows the sprite to move on forever
        """
        self.boundAction = action

    def setPosition (self, position):
        """ place the sprite directly at the given position
            expects an (x, y) tuple
        """
        (self.x, self.y) = position
        #update the rect
        self.rect.center = self.x, self.y
        
    def moveBy (self, vector):
        """ move the sprite by the (dx, dy) values in vector
            automatically calls checkBounds. Doesn't change 
            speed or angle settings.
        """
        (dx, dy) = vector
        self.x += dx
        self.y += dy
        self.__checkBounds()

    def forward(self, amt):
        """ move amt pixels in the current direction
            of travel
        """
        
        #calculate dx dy based on current direction
        radians = self.dir * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.x += dx
        self.y += dy
        
    def addForce(self, amt, angle):
        """ apply amt of thrust in angle.
            change speed and dir accordingly
            add a force straight down to simulate gravity
            in rotation direction to simulate spacecraft thrust
            in dir direction to accelerate forward
            at an angle for retro-rockets, etc.
        """

        #calculate dx dy based on angle
        radians = angle * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.dx += dx
        self.dy += dy
        self.updateVector()
        
    def updateVector(self):
        #calculate new speed and angle based on dx, dy
        #call this any time you change dx or dy
        
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        
        dy = self.dy * -1
        dx = self.dx
        
        radians = math.atan2(dy, dx)
        self.dir = radians / math.pi * 180

    def setSpeedLimits(self, max, min):
        """ determines maximum and minimum
            speeds you will allow through
            speedUp() method.  You can still
            directly set any speed you want
            with setSpeed() Default values:
                max: 10
                min: -3
        """
        self.maxSpeed = max
        self.minSpeed = min

    def dataTrace(self):
        """ utility method for debugging
            print major properties
            extend to add your own properties
        """
        #print "x: %d, y: %d, speed: %.2f, dir: %.f, dx: %.2f, dy: %.2f" % \
        #      (self.x, self.y, self.speed, self.dir, self.dx, self.dy)
        
        print(f"""
              x: {self.x}, y: {self.y}
              speed: {self.speed}, dir: {self.dir}
              dx: {self.dx}, dy: {self.dy}""")
            
    def mouseDown(self):
        """ boolean function. Returns True if the mouse is 
            clicked over the sprite, False otherwise
        """
        self.pressed = False
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True
        return self.pressed
    
    def clicked(self):
        """ Boolean function. Returns True only if mouse
            is pressed and released over sprite
            
        """
        released = False
        if self.pressed:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    released = True
            return released
        
    def collidesWith(self, target):
        """ boolean function. Returns True if the sprite
            is currently colliding with the target sprite,
            False otherwise
            Does not count collision if either sprite is hidden
        """
        collision = False
        if self.visible:
            if target.visible:
                if self.rect.colliderect(target.rect):
                    collision = True
        return collision
    
    def collidesGroup(self, target):
        """ wrapper for pygame.sprite.spritecollideany() function
            simplifies checking sprite - group collisions
            returns result of collision check (sprite from group 
            that was hit or None)
            Does not count collision if either sprite is hidden
            
        """
        if self.visible:
            collision = pygame.sprite.spritecollideany(self, target)
            if collision:
                if collision.visible:
                    return collision
                else:
                    return None
        
    def distanceTo(self, point):
        """ returns distance to any point in pixels
            can be used in circular collision detection
        """
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        
        dist = math.sqrt((dx * dx) + (dy * dy))
        return dist
    
    def dirTo(self, point):
        """ returns direction (in degrees) to 
            a point """
        
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        dy *= -1
        
        radians = math.atan2(dy, dx)
        dir = radians * 180 / math.pi
        dir += 180
        return dir
    
    def drawTrace(self, color=(0x00, 0x00, 0x00)):
        """ traces a line between previous position
            and current position of object 
        """
        pygame.draw.line(self.scene.background, color, self.oldCenter,
                         self.rect.center, 3)
        self.screen.blit(self.scene.background, (0, 0))

    def setSize(self, newX, newY):
        self.imageMaster = pygame.transform.scale(self.imageMaster, (newX, newY))
        
    def changeXby(self, value):
        self.x += value
        
    def changeYby(self, value):
        self.y += value

    def hide(self):
        self.oldPosition = self.rect.center
        self.setPosition((-1000, -1000))
        self.visible = False
        
    def show(self):
        self.visible = True
        self.setPosition(self.oldPosition)


if __name__ == "__main__":
    # change this code to test various features of the engine
    # This code will not run when gameEngine is run as a module
    # (as it usually will be)
        
    game = Scene()
    game.start()
