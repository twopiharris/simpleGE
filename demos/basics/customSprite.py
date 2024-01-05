import pygame, simpleGE
#customSprite.py

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
        
def main():
    game = simpleGE.Scene()
    game.player = Player(game)
    game.sprites = [game.player]
    game.start()

if __name__ == "__main__":
    main()

        
