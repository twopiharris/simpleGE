#multi-sprites
import pygame, simpleGE, random

class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("blue", (50, 50))
        self.x = 320
        self.y = 240
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed        
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        
class Target(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.colorRect("red", (25, 25))
        self.reset()
        
    def reset(self):
        self.x = random.randint(0, self.scene.background.get_width())
        self.y = random.randint(0, self.scene.background.get_height())
        self.moveAngle = random.randint(0, 360)
        self.speed = random.randint(0, 5)
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.targets = []
        for i in range(10):
            self.targets.append(Target(self))
            
        self.sprites = [self.player, self.targets]
        
    def process(self):
        for i in range(10):
            if self.player.collidesWith(self.targets[i]):
                self.targets[i].reset()               

def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()