import pygame, simpleGE

""" basicSpace.py 
    basic space physics
"""

class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("ship.gif")
        self.setSize(50, 30)
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(.5, self.imageAngle)
            

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.ship = Ship(self)
        
        self.sprites = [self.ship]
        

def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()