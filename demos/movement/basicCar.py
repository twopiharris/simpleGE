import pygame, simpleGE

""" Basic Car 
    turnBy and Forward
"""

class Car(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("car.png")
        self.setSize(30, 20)
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.turnBy(5)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.turnBy(-5)
        if self.isKeyPressed(pygame.K_UP):
            self.forward(5)
        if self.isKeyPressed(pygame.K_DOWN):
            self.forward(-3)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill("gray")
        self.car = Car(self)
        
        self.sprites = [self.car]
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    