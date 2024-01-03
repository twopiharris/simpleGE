""" asteroids.py 
    basic variation of the classic
    using simpleGE
    updated for Sprite 3.0
"""

import pygame, simpleGE, random

class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("shipSmall.gif")
        self.setAngle(0)
        self.speed = 0
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(.2, self.imageAngle)
        if self.isKeyPressed(pygame.K_SPACE):
            self.scene.bullet.fire()
    
class Bullet(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("bullet.gif")
        self.setSize(5, 5)
        self.setBoundAction(self.HIDE)
        self.reset()
        
    def fire(self):
        self.position = (self.scene.ship.x, self.scene.ship.y)
        self.speed = 12
        self.setAngle(self.scene.ship.imageAngle)
        
    def reset(self):
        self.position = (-100, -100)
        self.speed = 0
        
    
class Rock(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("rock.gif")
        self.reset()
        
    def process(self):
        self.imageAngle += self.rotSpeed
        
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.position = (x, y)
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("rock.gif")
        self.setSize(scale, scale)
        
        self.speed = random.randint(0, 6)
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 5)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        
        self.rocks = []
        for i in range(10):
            self.rocks.append(Rock(self))
            
        self.sprites = [self.bullet, self.ship, self.rocks]
        self.setCaption("asteroids")       
        
    def process(self):
        for rock in self.rocks:
            if self.ship.collidesWith(rock):
                rock.reset()
            if self.bullet.collidesWith(rock):
                rock.reset()
                self.bullet.reset()

def main():
    game = Game()    
    game.start()
    
if __name__ == "__main__":
    main()