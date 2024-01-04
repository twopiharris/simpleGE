import simpleGE, pygame

""" character.py 
    creating an animated character
    using sprites generated from LPC generator
    https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/
"""

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill(pygame.Color("papayawhip"))
        self.setCaption("Arrows to move player around screen")
        self.player = Player(self)
        
        self.sprites = [self.player]

class Anim():
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
          You can use more than one animation object if you have
          different cell sizes or counts.
        """
        
        self.imageFileName = "characterWalk.png"
        self.cellSize = (64, 64)        
        self.NUMROWS = numRows
        self.NUMCOLS = numCols
        self.delay = delay
        self.animRow = 0
        self.animCol = 0
        self.timer = simpleGE.Timer()
        self.startCol = 0

        self.animImage = pygame.image.load(self.imageFileName)
        self.animImage.convert_alpha()
        
    def getCellImage(self, row, col):
        """ given a row and column, returns the appropriate sub-image """
        imgOut = pygame.Surface(self.cellSize, pygame.SRCALPHA)
        
        cellWidth = self.cellSize[0]
        cellHeight = self.cellSize[1]
        
        cellX = row * cellWidth
        cellY = col * cellHeight
        
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

class Player(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim = Anim("characterWalk.png", (64, 64), 4, 9, .1)

        #in this animation, cell 0 is idle, so start at 1
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 2
        
    def checkEvents(self):
        self.setDX(0)
        self.setDY(0)
        walking = False
        
        if self.scene.isKeyPressed(pygame.K_UP):
            self.animRow = 0
            self.setDY(-self.moveSpeed)
            walking = True
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.animRow = 1
            self.setDX(-self.moveSpeed)
            walking = True
        if self.scene.isKeyPressed(pygame.K_DOWN):
            self.animRow = 2 
            self.setDY(self.moveSpeed)
            walking = True
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.animRow = 3 
            self.setDX(self.moveSpeed)
            walking = True

        if walking:        
            self.imageMaster = self.walkAnim.getNext(self.animRow)
        else:
            #use the current idle image
            self.imageMaster = self.walkAnim.getCellImage(0, self.animRow)

        self.rect = self.imageMaster.get_rect()
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
