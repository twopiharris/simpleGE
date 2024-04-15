""" collisionTest.py """

import pygame, simpleGE

class MovyThing(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("Green", (50, 50))
        
    def process(self):
        self.speed = 0
        #self.dir = "none"
        if self.isKeyPressed(pygame.K_a):
            self.dx = -5
            self.dir = "left"
        elif self.isKeyPressed(pygame.K_d):
            self.dx = 5
            self.dir = "right"
        elif self.isKeyPressed(pygame.K_w):
            self.dy = -5
            self.dir = "up"
        elif self.isKeyPressed(pygame.K_s):
            self.dir = "down"
            self.dy = 5

        #barrier check
        barrier = self.scene.barrier
        if self.collidesWith(barrier):
            if self.dir == "left":
                self.speed = 0
                if self.left <= barrier.right:
                    self.left = barrier.right
                    
            elif self.dir == "right":
                self.speed = 0
                if self.right >= barrier.left:
                    self.right = barrier.left
                    
            elif self.dir == "up":
                self.speed = 0
                if self.top <= barrier.bottom:
                    self.top = barrier.bottom
                    self.speed = 0
                    
            elif self.dir == "down":
                self.speed = 0
                if self.bottom >= barrier.top:
                    self.bottom = barrier.top
                    self.speed = 0
            

class DrivyThing(simpleGE.Sprite):
    
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("blue", (50, 20))
        #self.setSize(50, 50)
        self.setAngle(45)
        
    def process(self):
        
        if self.isKeyPressed(pygame.K_UP):
            self.speed += .1
        if self.isKeyPressed(pygame.K_DOWN):
            self.speed -= .1
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5 
            self.moveAngle += 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5 
            self.moveAngle -= 5
            
        if self.isKeyPressed(pygame.K_w):
            self.boundAction = self.WRAP
        elif self.isKeyPressed(pygame.K_b):
            self.boundAction = self.BOUNCE
            
        self.scene.lblOut.text = f"m: {self.moveAngle}, i: {self.imageAngle}"
        
        barrier = self.scene.barrier
        angle = self.moveAngle % 360
        if angle < 45:
            dir = "right"
        elif angle < 135:
            dir = "up"
        elif angle < 225:
            dir = "left"
        elif angle < 315:
            dir = "down"
        else:
            dir = "right"
        
        if self.collidesWith(barrier):

            if dir == "right":
                if self.right > barrier.left:
                    self.right = barrier.left  
                    self.speed = 0
            if dir == "left":
                if self.left < barrier.right:
                    self.left = barrier.right 
                    self.speed = 0    
            if dir == "down":
                if self.bottom > barrier.top:
                    self.bottom = barrier.top 
                    self.speed = 0
            if dir == "up":
                if self.top < barrier.bottom:
                    self.top = barrier.bottom 
                    self.speed = 0

class LblOut(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = (320, 30)
        self.size = (200, 30)
        self.fgColor = "blue"
        self.bgColor = "white"
        self.clearBack = True

class Game(simpleGE.Scene):
    
    """ used only for testing purposes. not a formal part of simpleGE """

    def __init__(self):
        super().__init__()
        self.background.fill("papayawhip")
        self.setCaption("WASD for green, arrows for blue")
        self.drivy = DrivyThing(self)
        self.movy = MovyThing(self)
        
        self.barrier = simpleGE.Sprite(self)
        self.barrier.colorRect("red", (100, 100))
        self.barrier.x = 320
        self.barrier.y = 240
        self.lblOut = LblOut()
        self.sprites = [self.lblOut, 
                        self.barrier,
                        self.movy,
                        self.drivy]
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()