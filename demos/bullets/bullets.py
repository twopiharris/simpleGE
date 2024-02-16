import pygame, simpleGE, random, space

""" bullet.py """

class Bullet(simpleGE.Sprite):
    def __init__(self, scene, parent):
        super().__init__(scene)
        self.parent = parent
        self.colorRect("white", (5, 5))
        self.setBoundAction(self.HIDE)
        self.hide()

    def fire(self):
        self.show()
        self.position = self.parent.position
        self.moveAngle = self.parent.imageAngle
        self.speed = 20
        
class Ship(space.Ship):
    def __init__(self, scene):
        super().__init__(scene)
        
    def process(self):
        super().process()
        """ press b key for a stream of bullets """
        if self.isKeyPressed(pygame.K_b):
            self.scene.currentBullet += 1
            if self.scene.currentBullet >= self.scene.NUM_BULLETS:
                self.scene.currentBullet = 0
            self.scene.bullets[self.scene.currentBullet].fire()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("arrows to control, space for bullet, b for bullet stream")
        self.ship = Ship(self)
        self.NUM_BULLETS = 100
        self.currentBullet = 0       
        self.bullets = []
        for i in range(self.NUM_BULLETS):
            self.bullets.append(Bullet(self, self.ship))
                                
        self.sprites = [self.ship, self.bullets]

    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.currentBullet += 1
                if self.currentBullet >= self.NUM_BULLETS:
                    self.currentBullet = 0
                self.bullets[self.currentBullet].fire()
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()

        
