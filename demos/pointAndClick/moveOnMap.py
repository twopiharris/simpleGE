import pygame, simpleGE

""" point and click
    various techniques for point and click
    
    pirate ship: https://opengameart.org/content/old-fashioned-pirate-ship
    map: https://opengameart.org/content/simple-map-tiles
    crosshair: https://opengameart.org/content/crosshair-pack-200%C3%97 
               kenney's crosshair pack
    """
    
    
class Ship(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("ship_parallax_complete.png")
        self.setSize(100, 50)
        self.position = (320, 240)
    
class Crosshair(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("crosshair010.png")
        self.setSize(50, 50)
        
        
    def process(self):
        (mx, my) = pygame.mouse.get_pos()
        self.x = mx
        self.y = my
        
    
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("example_map.png")
        #self.background = pygame.image.load("example_map.png")
        #self.background = pygame.transform.scale(self.background, (640, 480))
        
        #hide mouse pointer
        pygame.mouse.set_visible(False)
        
        self.ship = Ship(self)
        self.crosshair = Crosshair(self)
        
        self.sprites = [self.ship, self.crosshair]
        
    def process(self):
        # move until close to mouse position
        mousePos = pygame.mouse.get_pos()
        dist = self.ship.distanceTo(mousePos)
        mouseDir = self.ship.dirTo(mousePos)
        
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.ship.moveAngle = mouseDir
            self.ship.speed = 3
        else:
            self.ship.speed = 0
            
        if dist < 5:
            self.ship.speed = 0
        
def main():
    game = Game()
    game.start()
    pygame.mouse.set_visible(True)
    
    
if __name__ == "__main__":
    main()
    