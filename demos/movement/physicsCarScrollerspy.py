import pygame, simpleGE

""" physicsCar.py
    use more sophisticated physics system on car
"""

class ScrDrag(simpleGE.Scroller):
    def __init__(self):
        super().__init__()
        self.center = (100, 50)
        self.clearBack = True
        self.size = (250, 30)
        self.value = .05
        self.minValue = .02
        self.maxValue = .15
        self.increment = .01

    def process(self):
        self.text = f"<< drag: {self.value:10.2f} >>"

class ScrAccel(simpleGE.Scroller):
    def __init__(self):
        super().__init__()
        self.center = (100, 80)
        self.clearBack = True
        self.size = (250, 30)
        self.value = .5
        self.minValue = .1
        self.maxValue = 3.0
        self.increment = .1

    def process(self):
        self.text = f"<< accel: {self.value:10.2f} >>"

class ScrTurnRate(simpleGE.Scroller):
    def __init__(self):
        super().__init__()
        self.center = (100, 110)
        self.clearBack = True
        self.size = (250, 30)
        self.value = 5
        self.minValue = 1
        self.maxValue = 10
        self.increment = 1

    def process(self):
        self.text = f"<< turn: {self.value:12} >>"

class LblSpeed(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.center = (100, 140)
        self.fgColor = "black"
        self.clearBack = True
        self.text = "speed: 0"
        

class Car(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("car.png")
        self.setSize(30,20)
        self.position = (320, 240)
        self.drag = .05
        self.accel = .5
        self.turnRate = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.turnBy(self.turnRate)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.turnBy(-self.turnRate)
        if self.isKeyPressed(pygame.K_UP):
            self.addForce(self.accel, self.imageAngle)
            
        #compensate for drag.
        self.speed *= (1 - self.drag)
        
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill("gray")
        self.setCaption("adjust parameters with scrollers")
        
        #add some scrollers
        self.scrDrag = ScrDrag()
        self.scrAccel = ScrAccel()
        self.scrTurnRate = ScrTurnRate()
        self.lblSpeed = LblSpeed()
        
        
        self.car = Car(self)
        self.sprites = [self.car,
                        self.scrDrag,
                        self.scrAccel,
                        self.scrTurnRate,
                        self.lblSpeed]
        
    def process(self):
        self.car.drag = self.scrDrag.value
        self.car.accel = self.scrAccel.value
        self.car.turnRate = self.scrTurnRate.value
        self.lblSpeed.text = f"speed: {self.car.speed:.2f}"
        
def main():
    game = Game()
    game.start()
    
if __name__ == "__main__":
    main()