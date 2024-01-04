import pygame, simpleGE, space

""" joystick.py 
    demonstrate use of a basic joystick
"""

class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.images = {
            "cruise": pygame.image.load("shipCruise.png"),
            "left":   pygame.image.load("shipLeft.png"),
            "right":  pygame.image.load("shipRight.png"),
            "thrust": pygame.image.load("shipThrust.png")}
        self.copyImage(self.images["cruise"])
        self.setAngle(90)
        
    def process(self):
        self.copyImage(self.images["cruise"])
        joy = self.scene.joy
        axRotation = joy.get_axis(0)
        if axRotation < -.2:
            self.imageAngle += (axRotation * -5)
            self.copyImage(self.images["right"])
        if axRotation > .2:
            self.imageAngle += (axRotation * -5)
            self.copyImage(self.images["left"])    
        if joy.get_button(0) == 1:
            self.addForce(.2, self.imageAngle)
            self.copyImage(self.images["thrust"])
            
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Joysticks in space")
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)
        self.ship = Ship(self)
        
        self.sprites = [self.ship]
        
def main():
    game = Game()
    game.start()
        
    
if __name__ == "__main__":
    main()
    