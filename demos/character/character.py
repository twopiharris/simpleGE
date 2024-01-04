import simpleGE, pygame

""" character.py 
    creating an animated character
    using sprites generated from LPC generator
    https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator/
"""

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill(pygame.Color("papayawhip"))
        self.setCaption("Arrows to move player around screen")
        self.player = Player(self)
        
        self.sprites = [self.player]

class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim = simpleGE.SpriteSheet("characterWalk.png", (64, 64), 4, 9, .1)

        #in this animation, cell 0 is idle, so start at 1
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 2
        #self.copyImage(self.walkAnim.getCellImage(0, 0))
        
    def process(self):
        self.dx = 0
        self.dy = 0
        walking = False
        
        if self.isKeyPressed(pygame.K_UP):
            self.animRow = 0
            self.dy = -self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_LEFT):
            self.animRow = 1
            self.dx = -self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_DOWN):
            self.animRow = 2 
            self.dy = self.moveSpeed
            walking = True
        if self.isKeyPressed(pygame.K_RIGHT):
            self.animRow = 3 
            self.dx = self.moveSpeed
            walking = True

        if walking:        
            self.copyImage(self.walkAnim.getNext(self.animRow))
        else:
            #use the current idle image
            self.copyImage(self.walkAnim.getCellImage(0, self.animRow))

        #self.rect = self.imageMaster.get_rect()
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()
