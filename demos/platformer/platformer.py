""" platformer """

import pygame, simpleGE

class Charlie(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Charlie.png")
        self.setSize(50, 50)
        self.position = (50, 400)
        self.inAir = True
            
    def process(self):
        if self.inAir:
            self.addForce(.2, 270)
        
        if self.y > 450:
            self.inAir = False
            self.y = 450
            self.dy = 0          
        
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.x -= 5   
        if self.scene.isKeyPressed(pygame.K_UP):
            if not self.inAir:
                self.addForce(6, 90)
                self.inAir = True

        self.inAir = True
        for platform in self.scene.platforms:
            if self.collidesWith(platform):                
                if self.dy > 0:
                        self.bottom = platform.top
                        self.dy = 0
                        self.inAir = False
        
class Platform(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.colorRect("darkblue", (50, 50))
       
    def update(self):
        super().update()
        if self.mouseDown:
            self.position = pygame.mouse.get_pos()

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("arrows to move and jump. drag platforms around")

        self.charlie = Charlie(self)

        self.platforms = [Platform(self, (100, 450)), 
                          Platform(self, (150, 450)), 
                          Platform(self, (200, 450)), 
                          Platform(self, (250, 450)),
                          Platform(self, (300, 350)), 
                          Platform(self, (350, 350))]
        self.sprites = [self.platforms, self.charlie]
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    