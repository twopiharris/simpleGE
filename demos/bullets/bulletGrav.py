import pygame, simpleGE, math

""" bullets with gravity """


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
            self.speed = self.scene.scrVelocity.value

    def process(self):
        if self.visible:
            #self.dy += 1
            self.addForce(1, 270)
        else:
            self.speed = 0
        
class Gun(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("turret.gif")
        self.position = (30, 450)
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.imageAngle += 5
        if self.isKeyPressed(pygame.K_RIGHT):
            self.imageAngle -= 5
        if self.isKeyPressed(pygame.K_UP):
            scroller = self.scene.scrVelocity
            if scroller.value < scroller.maxValue:
                scroller.value += 1
        if self.isKeyPressed(pygame.K_DOWN):
            scroller = self.scene.scrVelocity
            if scroller.value > scroller.minValue:
                scroller.value -= 1            
        if self.isKeyPressed(pygame.K_SPACE):
            self.scene.bullet.fire()

class ScrVelocity(simpleGE.Scroller):
    def __init__(self):
        super().__init__()
        self.minValue = 0
        self.maxValue = 30
        self.value = 15
        self.center = ((200, 450))

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.gun = Gun(self)
        self.bullet = Bullet(self, self.gun)
        self.scrVelocity = ScrVelocity()

        self.sprites = [self.bullet, self.gun, self.scrVelocity]
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()