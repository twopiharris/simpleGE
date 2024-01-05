import pygame, simpleGE

""" tileCollision.py
    demonstrate basic tbw 
    tile images from lpc Atlas - openGameArt
    http://opengameart.org/content/lpc-tile-atlas
    """
   
class LblOutput(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = (320, 25)
        self.text = "current tile: "
        self.fgColor = "white"
        self.bgColor = "black"
        self.clearBack = True
    
class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("red", (20, 20))
        self.moveSpeed = 2

    def process(self):
        
        #standard motion
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
        # look for a target tile
        if self.tileOver == (12, 19):
            self.imageMaster.fill("white")
        else:
            self.imageMaster.fill("red")
            
        #adjust movement speed by terrain
        if self.tileState == "0":
            self.moveSpeed = 2
        elif self.tileState == 1:
            self.moveSpeed = 4
        elif self.tileState == 2:
            self.moveSpeed = .2
        else:
            self.moveSpeed = 2
        
class Tile(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = [
            pygame.image.load("grass.png"),
            pygame.image.load("dirt.png"),
            pygame.image.load("water.png")]
        
        self.stateName = ["grass", "dirt", "water"]
        
        self.setSize(32, 32)
        self.GRASS = 0
        self.DIRT = 1
        self.WATER = 2
        self.state = self.GRASS
        self.clicked = False
        self.active = False
        
    def setState(self, state):
        self.state = state
        self.copyImage(self.images[state])

    def process(self):
        
        #allow editing
        if self.clicked:
            newState = self.state + 1
            if newState > 2:
                newState = 0
            self.setState(newState)    
            
        # look for player
        if self.collidesWith(self.scene.player):
            stateInfo = self.stateName[self.state]
            self.scene.player.tileOver = self.tilePos
            self.scene.player.tileState = self.state
            rowCol = f"{self.tilePos[0]}, {self.tilePos[1]}"
            
            self.scene.lblOutput.text = f"{stateInfo} {rowCol}"
            
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Click on a tile to edit, arrows to move")
        self.tileset = []
        
        self.ROWS = 15
        self.COLS = 20
        
        self.loadMap()
        
        self.player = Player(self)
        self.lblOutput = LblOutput()
        
        self.sprites = [self.tileset, self.player, self.lblOutput]
        
    def loadMap(self):
        
      map = [
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],  
          [2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],  
          [2,2,2,2,2,2,0,0,0,0,1,0,0,0,0,0,2,2,2,2],  
          [0,2,2,2,2,2,2,0,0,0,1,0,0,0,2,2,2,2,2,0],  
          [0,0,0,0,0,0,2,2,2,2,1,2,2,2,2,2,0,0,0,0],  
          [0,0,0,0,0,0,0,2,2,2,1,2,2,2,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]  
      ]
    
      for row in range(self.ROWS):
          self.tileset.append([])
          for col in range(self.COLS):
            currentVal = map[row][col]
            newTile = Tile(self)
            newTile.setState(currentVal)
            newTile.tilePos = (row, col)
            xPos = 16 + (32 * col)
            yPos = 16 + (32 * row)
            newTile.x = xPos
            newTile.y = yPos
            self.tileset[row].append(newTile)

                
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()