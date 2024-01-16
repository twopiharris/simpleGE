import pygame, simpleGE

""" physicsCar.py
    use more sophisticated physics system on car
"""

class Car(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("car.png")
        self.setSize(30,20)
        self.drag = .05
        self.accel = .5
        self.turnRate = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.turnBy(self.turnRate)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.turnBy(-self.turnRate)
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(self.accel, self.imageAngle)
            
        #compensate for drag.
        self.speed *= (1 - self.drag)
        
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