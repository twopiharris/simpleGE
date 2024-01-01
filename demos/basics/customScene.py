#CustomScene.py

import pygame, simpleGE

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.box = simpleGE.Sprite(self)
        self.box.dx = 5
        
        self.sprites = self.box

def main():
    game = Game()
    game.start()
    
    
if __name__ == "__main__":
    main()