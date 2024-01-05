#states
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
        self.clearBack = True
        self.center = (50, 20)
        self.size = (150, 30)
        
        
class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time"
        self.center = (550, 20)
        self.size = (150, 30)
        self.clearBack = True
        self.fgColor = "white"
        self.bgColor = "black"       
        
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
        
        self.sprites = [self.player, 
                        self.targets,
                        self.lblScore, 
                        self.lblTimer]
        
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

class Instructions(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.lblInstructions = simpleGE.MultiLabel()
        self.lblInstructions.center = (320, 240)
        self.lblInstructions.size = (400, 300)
        self.lblInstructions.textLines = [
            "Move the blue box with the arrow",
            "keys.",
            "See how many red boxes you can catch",
            "before you run out of time.",
            "",
            "Click to start."
        ]
        
        self.sprites = [self.lblInstructions]
        
        
    def process(self):
        if self.lblInstructions.clicked:
            self.stop()

class GameOver(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        
        self.score = 0
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Score: {self.score}"
        self.lblScore.center = (320, 140)

        self.btnAgain = simpleGE.Button()
        self.btnAgain.text = "Play again"
        self.btnAgain.center = (150, 250)

        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (450, 250)

        self.sprites = [self.lblScore, self.btnAgain, self.btnQuit]

        
    def setScore(self, score):
        self.score = score
        self.lblScore.text = f"Score: {self.score}"

    def process(self):
        if self.btnAgain.clicked:
            self.next = "again"
            self.stop()
            
        if self.btnQuit.clicked:
            self.next = "quit"
            self.stop()

def main():
    
    keepGoing = True
    while (keepGoing):
        instructions = Instructions()
        instructions.start()
        
        game = Game()
        game.start()
        
        gameOver = GameOver()
        gameOver.setScore(game.score)
        gameOver.start()

        if gameOver.next == "quit":
            keepGoing = False

if __name__ == "__main__":
    main()