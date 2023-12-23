# simpleGE
 
## Overview

New programmers are very interested in game development, but arcade games can be 
extremely difficult for new programmers to write.  Scratch is a powerful and popular tool for beginners, but the tile-based programming has limitations, and does not always feel like 'real' programming in a traditional language.  More powerful graphics APIs like Pygame are extremely powerful, but can be very complex for beginners.  Stock pygame requires a fair amount of math and programming skill to use well.  A number of attempts to simplify pygame have been created for educational purposes (specifically pygame zero.)  However, when examining this tool for use in an educational setting, I found it to be too limiting.  Specifically, it did not allow for rotating sprites or sprite sheet animation.  

SimpleGE is derived from two previous engines I wrote for various books and teaching experiences.  It is designed to be powerful, flexible, and reasonably easy to use. It has a relatively small number of objects to learn, but you can use it to make a surprising range of 2D games.

## The Scene
The primary class in simpleGE is the scene.  If you've tried to write pygame code, you end up writing the same (somewhat mystic) main code every time.  The scene class manages all of this, allowing you to create an object that encapsulates the screen and the timing system.  You can use the Scene class as-is, or you can subclass it to create your own custom scenes.  You can have as many scenes as you want in your game, so you can build separate scenes for instructions, game play, multiple levels of your game, and end-of game summaries.  

## The Sprite
The sprite class is the foundational class in simpleGE.  It is based on the pygame Sprite, so you can still do everything you could do with the pygame sprite.  But it is quite a bit easier to use and more powerful. It has a number of convenience features.
* **position properties** - Just assign a new value to x or y to move the sprite immediately.  In addition, you can read and write the top, bottom, left, and right properties of the sprite.
*  **motion properties** - you can move the object by changing its dx and dy properties, or set a moveAngle and speed, and the sprite will calculate dx and dy automatically.
*  **add force** - The add force method allows you to apply a force vector at any speed and angle to your sprite.  This allows for realistic gravity and other physics effects.
*  **angles** - The sprite has two main angle measurements.  The imageAngle is the visual rotation, and the moveAngle allows you to move in an arbitrary direction.  You can set these properties seperately (for a spaceship that moves sideways, for example) or you can use the ordinary angle property to handle both types of angle at once.
*  **event-handling** - the Sprite has a process() method, which is empty.  Any code you put in the process method will happen every frame.  The isKeyPressed() method provides for easy keyboard reading, and you have access to attributes determining whether the mouse is over a sprite, pressed on a sprite, or has clicked on the sprite.
*  **collision management** - The collidesWith() method checks to see if this sprite has collided with another sprite.  You can also use the dirTo() and distanceTo() methods to implement a circular collision system, or to point the sprite towards a mouse or other sprite.

## GUI Elements
SimpleGE also includes a small but powerful set of GUI tools.  These are sufficient for building a basic user interface with both input and output widgets.  All widgets can have a customized foreground and background color, custom font, size and position. All widgets can be used as-is or subclassed for more specific behavior.
* **Label** - A basic output label, good for scores, timing, and other simple information.
* **MultiLabel** - a multi-line label, useful for instructions or other multi-line output.
* **Button** - just like a label, but you can click on it.  You can test whether the button has been clicked for input
* **Scroller** - a simple but functional scroller for error-free numeric input.  You can specify the range of values as well as how the values change
* **TextInput** - a basic but functional text box.  Allows for text input

## Convenience classes
SimpleGE comes with a few other classes to help write fun games.
* **Timer** - The timer is used for, well, timing. You can have as many as you want without affecting performance.
* **Sound** - an object to simplify sound effects
* **Animation** - an object to easily convert a spritesheet into a character animation.  Can also be used to extract tiles from a tilesheet for use in a tile-based world.

