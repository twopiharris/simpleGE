import pygame, simpleGE

""" space.py 
    illustrates space movement using simpleGE
    ship images modified from Ari's spritelib.
"""

class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = {
            "cruise": pygame.image.load("shipCruise.png"),
            "left":   pygame.image.load("shipLeft.png"),
            "right":  pygame.image.load("shipRight.png"),
            "thrust": pygame.image.load("shipThrust.png")}
        self.copyImage(self.images["cruise"])
        
    def process(self):
        self.copyImage(self.images["cruise"])
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5
            self.copyImage(self.images["right"])
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5
            self.copyImage(self.images["left"])    
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(.2, self.imageAngle)
            self.copyImage(self.images["thrust"])
            
def main():
    game = simpleGE.Scene()
    game.setCaption("Pygame in SPAAAAACE!")
    ship = Ship(game)
    game.sprites = [ship]
    game.start()
    
if __name__ == "__main__":
    main()

