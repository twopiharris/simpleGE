import pygame, simpleGE, random

""" petals around the rose
    fun dice game / puzzle 
    
    dice image original: https://opengameart.org/content/dice-4
    dice sound original: https://opengameart.org/content/multiple-dice-rolling
    background music: https://opengameart.org/content/no-without-my-dice
    background image: https://opengameart.org/content/tavern-background
    """
    
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Tavern800x600.png")
        self.setCaption("How many petals around the rose?")
        
        self.sndRoll = simpleGE.Sound("diceRoll.wav")
        pygame.mixer.music.load("bgm.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1)
        
        self.dice = []
        for i in range(5):
            newDie = Die(self)
            newDie.position = (80 + (i * 120), 120)
            self.dice.append(newDie)
            
        self.btnRoll = BtnRoll()
        self.lblResult = LblResult()
        self.btnReveal = BtnReveal()
        
        self.sprites = [self.dice, self.btnRoll, self.lblResult, 
                        self.btnReveal]
    
    def process(self):
        if self.btnRoll.clicked:
            self.sndRoll.play()
            totalPetals = 0
            for die in self.dice:
                die.roll()
                totalPetals += die.nPetals
                
            self.lblResult.hide()
            self.lblResult.text = f"{totalPetals} petals around the rose"
        
        if self.btnReveal.clicked:
            self.lblResult.show((320, 310))
            
class Die(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)  
        
        self.setImage("1_dot.png")
        self.setSize(80, 80)
        
        self.images = [None,
                       pygame.image.load("1_dot.png"),
                       pygame.image.load("2_dots.png"),
                       pygame.image.load("3_dots.png"),
                       pygame.image.load("4_dots.png"),
                       pygame.image.load("5_dots.png"),
                       pygame.image.load("6_dots.png"),
                       ]
        for i in range(1, 7):
            self.images[i] = pygame.transform.scale(self.images[i], (80, 80))
                    
    def roll(self):
        self.value = random.randint(1, 6)
        self.copyImage(self.images[self.value])
        if self.value == 3:
            self.nPetals = 2
        elif self.value == 5:
            self.nPetals = 4
        else:
            self.nPetals = 0
        
class BtnRoll(simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.center = ((320, 240))
        self.text = "Roll 'em"

class LblResult(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = ((320, 310))
        self.text = "0 petals around the rose"
        self.size = ((250, 30))

class BtnReveal(simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.center = ((320, 410))
        self.text = "Reveal"

def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
    