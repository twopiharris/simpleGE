import pygame, simpleGE

""" testJoystick 
    simple utility to check joystick
    values.  Current values of all
    buttons and axes will appear in console
    Nothing is intended to appear on screne
    but simpleGE scene is still used for convenience
"""

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setCaption("Joystick test: Check console for joystick values")
        pygame.joystick.init()
        self.joy = pygame.joystick.Joystick(0)

    def doEvents(self, event):
        axes = self.joy.get_numaxes()
        for i in range(axes):
            axis = self.joy.get_axis(i)
            print(f"Axis {i}: {axis:.3f}")
            
        numButtons = self.joy.get_numbuttons()
        for i in range(numButtons):
            button = self.joy.get_button(i)
            print(f"Button {i}: {button}")

def main():
    game = Game()
    game.start()
        
    
if __name__ == "__main__":
    main()
    