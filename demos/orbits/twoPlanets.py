""" twoPlanets.py
    demonstrates complex orbit around two objects!
"""

import pygame, math
pygame.init()

class Ship(pygame.sprite.Sprite):
    def __init__(self, screen, background):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.background = background
        
        self.imageThrust = pygame.image.load("shipThrust.png")
        self.imageThrust = self.imageThrust.convert()
        self.imageCruise = pygame.image.load("shipCruise.png")
        self.imageCruise = self.imageCruise.convert()
        self.imageLeft = pygame.image.load("shipLeft.png")
        self.imageLeft = self.imageLeft.convert()
        self.imageRight = pygame.image.load("shipRight.png")
        self.imageRight = self.imageRight.convert()
        
        self.imageMaster = self.imageCruise
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        
        self.x = 320
        self.y = 150
        self.dx = 2
        self.dy = 0
        self.dir = 0
        self.turnRate = 5
        self.thrust = 0
        self.mass = 1
        
    def update(self):
        self.checkKeys()
        self.rotate()
        self.calcVector()
        self.setPos()
        #self.checkBounds()
        self.rect.center = (self.x, self.y)
        
    def checkKeys(self):
        keys = pygame.key.get_pressed()
        self.imageMaster = self.imageCruise
        if keys[pygame.K_RIGHT]:
            self.dir -= self.turnRate
            if self.dir < 0:
                self.dir = 360 - self.turnRate
            self.imageMaster = self.imageRight
        if keys[pygame.K_LEFT]:
            self.dir += self.turnRate
            if self.dir > 360:
                self.dir = self.turnRate
            self.imageMaster = self.imageLeft
            
        #clear background on spacebar
        if keys[pygame.K_SPACE]:
            self.background.fill((0, 0, 0))
        if keys[pygame.K_UP]:
            self.thrust = .1
            self.imageMaster = self.imageThrust
        else:
            self.thrust = 0
        
    def rotate(self):
        oldCenter = self.rect.center
        self.image = pygame.transform.rotate(self.imageMaster, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

    def calcVector(self):
        radians = self.dir * math.pi / 180
        
        thrustDx = self.thrust * math.cos(radians)
        thrustDy = self.thrust * math.sin(radians)
        thrustDy *= -1
        
        self.dx += thrustDx
        self.dy += thrustDy
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        
    def setPos(self):
        oldCenter = (self.x, self.y)
        self.x += self.dx
        self.y += self.dy
    
        pygame.draw.line(self.background, (0xFF, 0xFF, 0xFF), (oldCenter), (self.x, self.y))

    def checkBounds(self):
        screen = self.screen
        
        if self.x > screen.get_width():
            self.x = 0
        if self.x < 0:
            self.x = screen.get_width()
        if self.y > screen.get_height():
            self.y = 0
        if self.y < 0:
            self.y = screen.get_height()

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pluto.gif")
        self.image = self.image.convert()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.mass = 500
        self.x = 320
        self.y = 240
        self.rect.center = (self.x, self.y)

    def gravitate(self, body):
        """ calculates gravitational pull on 
            object """
        
        (self.x, self.y) = self.rect.center       
        #get dx, dy, distance
        dx = self.x - body.x
        dy = self.y - body.y
        
        distance = math.sqrt((dx * dx) + (dy * dy))
       
        #normalize dx and dy
        dx /= distance
        dy /= distance
        
        force = (body.mass * self.mass)/(math.pow(distance, 2))
        
        dx *= force
        dy *= force
        
        body.dx += dx
        body.dy += dy

def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Orbit - space bar to clear trail")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    ship = Ship(screen, background)
    planet = Planet()
    planet2 = Planet()
    planet2.rect.center = (450, 200)
    planet2.mass = 600
    allSprites = pygame.sprite.Group(ship, planet, planet2)
    
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
        
        planet.gravitate(ship)
        planet2.gravitate(ship)
        
        #allSprites.clear(screen, background)
        #re-blit background for drawing command
        screen.blit(background, (0, 0))
        
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()
    pygame.quit()
        
if __name__ == "__main__":
    main()