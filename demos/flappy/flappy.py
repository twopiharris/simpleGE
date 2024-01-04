import pygame, simpleGE, random

""" flappy.py 
    basic flappy bird prototype """
    
class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Charlie.png")
        self.setSize(50, 50)
        self.position = (100, 100)       
    
    def process(self):
        self.addForce(.1, 270)
        if self.scene.isKeyPressed(pygame.K_SPACE):
            self.dy = 0
            self.addForce(5, 90)    

class Barrier(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("green", (80, 200))
        self.position = (600, 0)    
        self.dx = -3
        
    def checkBounds(self):
        #only check for leave left
        if self.x < 0:
            self.scene.reset()
            
    def process(self):
        if self.collidesWith(self.scene.charlie):
            self.scene.reset() 
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.charlie = Charlie(self)
        self.upperBarrier = Barrier(self)
        self.lowerBarrier = Barrier(self)
        self.gap = 400
        self.reset()
        self.sprites = [self.charlie, self.upperBarrier, self.lowerBarrier]
        
    def reset(self):        
        self.topPosition = random.randint(0, 200)
        self.bottomPosition = self.topPosition + self.gap
        self.upperBarrier.position = (640, self.topPosition)
        self.lowerBarrier.position = (640, self.bottomPosition)
        
    
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    
        