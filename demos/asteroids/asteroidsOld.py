""" asteroids.py 
    basic variation of the classic
    using simpleGE
"""

import pygame, simpleGE, random

class Ship(simpleGE.SuperSprite):
    def __init__(self, scene):
        simpleGE.SuperSprite.__init__(self, scene)
        self.setImage("shipSmall.gif")
        self.setSpeed(0)
        self.setAngle(0)
        
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotateBy(5)
        if keys[pygame.K_RIGHT]:
            self.rotateBy(-5)
        if keys[pygame.K_UP]:
            self.addForce(.2, self.rotation)
        if keys[pygame.K_SPACE]:
            self.scene.bullet.fire()
    
class Bullet(simpleGE.SuperSprite):
    def __init__(self, scene):
        simpleGE.SuperSprite.__init__(self, scene)
        self.setImage("bullet.gif")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (5, 5))
        self.setBoundAction(self.HIDE)
        self.reset()
        
    def fire(self):
        self.setPosition((self.scene.ship.x, self.scene.ship.y))
        self.setSpeed(12)
        self.setAngle(self.scene.ship.rotation)
        
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)
        
    
class Rock(simpleGE.SuperSprite):
    def __init__(self, scene):
        simpleGE.SuperSprite.__init__(self, scene)
        self.setImage("rock.gif")
        self.reset()
        
    def checkEvents(self):
        self.rotateBy(self.rotSpeed)
        
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        self.setPosition((x, y))
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("rock.gif")
        self.imageMaster = \
            pygame.transform.scale(self.imageMaster, (scale, scale))
        
        self.setSpeed(random.randint(0, 6))
        self.setAngle(random.randint(0, 360))
        self.rotSpeed = random.randint(-5, 5)

class Game(simpleGE.Scene):
    def __init__(self):
        simpleGE.Scene.__init__(self)
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        
        self.rocks = []
        for i in range(10):
            self.rocks.append(Rock(self))
            
        self.rockGroup = self.makeSpriteGroup(self.rocks)
        self.addGroup(self.rockGroup)
        self.sprites = [self.bullet, self.ship]
        self.setCaption("asteroids")       
        
    def update(self):
        rockHitShip = self.ship.collidesGroup(self.rocks)
        if rockHitShip:
            rockHitShip.reset()

        rockHitBullet = self.bullet.collidesGroup(self.rocks)
        if rockHitBullet:
            rockHitBullet.reset()
            self.bullet.reset()
    
def main():
    game = Game()    
    game.start()
    
if __name__ == "__main__":
    main()