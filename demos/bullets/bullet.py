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
        # allow only one bullet at a time
        if not self.visible:
            self.show()
            self.position = self.parent.position
            self.moveAngle = self.parent.imageAngle
            self.speed = 20
        
class Ship(space.Ship):
    def __init__(self, scene):
        super().__init__(scene)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.ship = Ship(self)
        self.bullet = Bullet(self, self.ship)
        self.sprites = [self.ship, self.bullet]
        
        #self.bullets

    def doEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bullet.fire()
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()

        