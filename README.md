# simpleGE
 
## Overview

New programmers are very interested in game development, but arcade games can be 
extremely difficult for new programmers to write.  Scratch is a powerful and popular tool for beginners, but the tile-based programming has limitations, and does not always feel like 'real' programming in a traditional language.  More powerful graphics APIs like Pygame are extremely powerful, but can be very complex for beginners.  Stock pygame requires a fair amount of math and programming skill to use well.  A number of attempts to simplify pygame have been created for educational purposes (specifically pygame zero.)  However, when examining this tool for use in an educational setting, I found it to be too limiting.  Specifically, it did not allow for rotating sprites or sprite sheet animation.  

SimpleGE is derived from two previous engines I wrote for various books and teaching experiences.  It is designed to be powerful, flexible, and reasonably easy to use. It has a relatively small number of objects to learn, but you can use it to make a surprising range of 2D games.

## The Scene
The primary class in simpleGE is the scene.  If you've tried to write pygame code, you end up writing the same (somewhat mystic) main code every time.  The scene class manages all of this, allowing you to create an object that encapsulates the screen and the timing system.  You can use the Scene class as-is, or you can subclass it to create your own custom scenes.  You can have as many scenes as you want in your game, so you can build separate scenes for instructions, game play, multiple levels of your game, and end-of game summaries.  

## The Sprite
The sprite class is the foundational class in simpleGE.  It is based on the pygame Sprite, so you can still do everything you could do with the pygame sprite.  But it is quite a bit easier to use and more powerful.
