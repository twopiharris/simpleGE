#GUI
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
        
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.fgColor = "white"
        self.bgColor = "black"
        self.text = "Score"
        self.center = (50, 20)
        self.size = (150, 30)
        
    def update(self):
        super().update()
        self.image.set_colorkey(self.bgColor)
        
        
class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time"
        self.center = (550, 20)
        self.size = (150, 30)        
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.targets = []
        for i in range(10):
            self.targets.append(Target(self))
        
        self.lblScore = LblScore()    
        self.lblTimer = LblTimer()
        
        self.score = 0
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 15
        
        self.sprites = [self.lblScore, 
                        self.lblTimer, 
                        self.player, 
                        self.targets]
        
    def process(self):
        #check for collisions
        for i in range(10):
            if self.player.collidesWith(self.targets[i]):
                self.targets[i].reset()
                self.score += 100
                self.lblScore.text = f"Score {self.score}"
        
        #check time
        timeLeft = self.timer.getTimeLeft()
        self.lblTimer.text = f"Time Left: {timeLeft:.2f}"
        if timeLeft < 0:
            self.stop()        

def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()