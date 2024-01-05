import pygame, simpleGE

""" hotspot.py
    demonstrates hot spots on a point and click map
    map: https://opengameart.org/content/simple-map-tiles
    
"""

class HotSpot(simpleGE.Sprite):
    """ defines a rectangular area that can be 
        active or clicked.  By default, it is 
        semi-transparent white.  Once you have 
        positioned it, set transparent to True """
    
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect((255, 255, 255), (100, 100))
        self.transparent = False
        
    def process(self):

        #check for transparency
        if self.transparent:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(100)
                    
    def setPosition(self, position):
        self.x = position[0]
        self.y = position[1]
        self.rect = self.image.get_rect()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("example_map.png")
        self.setCaption("Find the hot spots - space to toggle hotspot visibility")
        
        self.hsVolcano = HotSpot(self)
        self.hsVolcano.setSize(110, 100)
        self.hsVolcano.position = (120, 80)
        self.hsVolcano.transparent = True

        self.hsTree = HotSpot(self)
        self.hsTree.position = (400, 200)
        self.hsTree.setSize(100, 130)
        self.hsTree.transparent = True
        
        self.lblOutput = simpleGE.Label()
        self.lblOutput.center = ((320, 400))
        self.lblOutput.text = ""
        
        self.sprites = [self.hsVolcano, self.hsTree, self.lblOutput]
        
    def process(self):
        self.lblOutput.text = ""
        if self.hsVolcano.mouseOver:
            self.lblOutput.text = "Volcano"
        if self.hsTree.mouseDown:
            self.lblOutput.text = "Tree"
            
        if self.hsVolcano.clicked:
            print("You clicked on the volcano")
            
        if self.hsTree.clicked:
            print("You clicked on the tree")
            
    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.hsTree.transparent = not self.hsTree.transparent
                self.hsVolcano.transparent = not self.hsVolcano.transparent
      
def main():
    game = Game()
    game.start()
    
    
if __name__ == "__main__":
    main()
        
       
