import pygame, simpleGE

""" tileScroll.py
    demonstrate basic tbw 
    tile images from lpc Atlas - openGameArt
    http://opengameart.org/content/lpc-tile-atlas
"""
    
class Tile(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = [
            pygame.image.load("grass.png"),
            pygame.image.load("dirt.png"),
            pygame.image.load("water.png")]
        
        self.setSize(32, 32)
        self.GRASS = 0
        self.DIRT = 1
        self.WATER = 2
        self.state = self.GRASS
    
    def setState(self, state):
        self.state = state
        self.copyImage(self.images[state])

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("arrows to scroll map")
        self.tileset = []
        
        self.ROWS = 20
        self.COLS = 40
        
        self.SCREEN_ROWS = 15
        self.SCREEN_COLS = 20
        
        self.offRow = 0
        self.offCol = 0
        
        self.loadMap()
        
        self.sprites = [self.tileset]
        
    def loadMap(self):
        
      self.map = [
          
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [2,2,2,2,2,2,0,0,0,0,1,0,0,0,0,0,2,2,2,2,2,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
          [0,2,2,2,2,2,2,0,0,0,1,0,0,0,2,2,2,2,2,0,0,0,0,0,2,2,0,0,1,1,1,1,1,0,0,0,0,0,0,0],  
          [0,0,0,0,0,0,2,2,2,2,1,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,1,1,1,0,0,0,0],  
          [0,0,0,0,0,0,0,2,2,2,1,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,2,2,1,0,0,0],  
          [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,1,0,0,0],  
          [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2,1,1,1],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,2,2,2,2,2,2,2,2,2,2],  
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2]
      ]
    
      for row in range(self.SCREEN_ROWS):
          self.tileset.append([])
          for col in range(self.SCREEN_COLS):
            newTile = Tile(self)
            newTile.setState(0)
            xPos = 16 + (32 * col)
            yPos = 16 + (32 * row)
            newTile.x = xPos
            newTile.y = yPos
            self.tileset[row].append(newTile)
            
    def showMap(self):
        """ shows a subset of the map SCREEN_ROWS by SCREENCOLS
            offset by offRow, offCol """
            
        for row in range(self.SCREEN_ROWS):
            for col in range(self.SCREEN_COLS):
                currentVal = self.map[row + self.offRow][col + self.offCol]
                self.tileset[row][col].setState(currentVal)
                
    def update(self):
        if self.isKeyPressed(pygame.K_LEFT):
            if self.offCol > 0:
                self.offCol -= 1
                
        if self.isKeyPressed(pygame.K_RIGHT):
            if self.offCol < self.COLS - self.SCREEN_COLS:
                self.offCol += 1
                
        if self.isKeyPressed(pygame.K_UP):
            if self.offRow > 0:
                self.offRow -= 1
                
        if self.isKeyPressed(pygame.K_DOWN):
            if self.offRow < (self.ROWS - self.SCREEN_ROWS):
                self.offRow += 1
                
        self.showMap()
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
