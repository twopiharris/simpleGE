import pygame, simpleGE, random

"""
xyMotion.py

Basics of axis-aligned motion

x, y, dx, dy, moveAngle, speed

"""

class Player(simpleGE.Sprite):
    """ player is stationary.
        process method directly changes x and y
    """
    
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Charlie.png")
        self.setSize(50, 50)
        self.position = (self.screenWidth/2, self.screenHeight/2)
        self.moveSpeed = 5
        self.setBoundAction(self.WRAP)

    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
            
class YellowBox(simpleGE.Sprite):
    """ randomize dx and dy to get random
        motion
    """
    
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("yellow", (50, 50))
        self.setBoundAction(self.BOUNCE)
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screenWidth)
        self.y = random.randint(0, self.screenHeight)
        self.dx = random.randint(-5, 5)
        self.dy = random.randint(-5, 5)
        
class BlueBox(simpleGE.Sprite):
    """ speed and moveAngle used to generate
        dx and dy automatically
    """
    
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("blue", (50, 50))
        self.setBoundAction(self.BOUNCE)
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.screenWidth)
        self.y = random.randint(0, self.screenHeight)
        self.speed = random.randint(1, 5)
        self.moveAngle = random.randint(0, 359)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Bonk into the boxes")
        
        self.player = Player(self)
        self.yellowBox = YellowBox(self)
        self.blueBox = BlueBox(self)
        
        self.sprites = [
            self.player,
            self.yellowBox,
            self.blueBox]
         
    def process(self):       
        
        if self.player.collidesWith(self.yellowBox):
            self.yellowBox.reset()
            
        if self.player.collidesWith(self.blueBox):
            self.blueBox.reset()
            
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    
        
        
        