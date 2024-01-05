# simpleGE Overview

New programmers are very interested in game development, but arcade games can be 
extremely difficult for new programmers to write.  Scratch is a powerful and popular tool for beginners, but the tile-based programming has limitations, and does not always feel like 'real' programming in a traditional language.  More powerful graphics APIs like Pygame are extremely powerful, but can be very complex for beginners.  Stock pygame requires a fair amount of math and programming skill to use well.  A number of attempts to simplify pygame have been created for educational purposes (specifically pygame zero.)  However, when examining this tool for use in an educational setting, I found it to be too limiting.  Specifically, it did not allow for rotating sprites or sprite sheet animation.  The larger gameDev tools like Unity, Unreal, and Godot can be very intimidating, and none uses stock Python.

SimpleGE is derived from two previous engines I wrote for various books and teaching experiences.  It is designed to be powerful, flexible, and reasonably easy to use. It has a relatively small number of objects to learn, but you can use it to make a surprising range of 2D games. It is a very light package, and runs fine on raspberry pis and chromebooks.

## The Scene
The primary class in simpleGE is the scene.  If you've tried to write pygame code, you end up writing the same (somewhat mystic) main code every time.  The scene class manages all of this, allowing you to create an object that encapsulates the screen and the timing system.  You can use the Scene class as-is, or you can subclass it to create your own custom scenes.  You can have as many scenes as you want in your game, so you can build separate scenes for instructions, game play, multiple levels of your game, and end-of game summaries.  The Scene class can be used as-is, or can be subclassed for more flexibility.

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

# Documentation

## Scene
The scene encapsulates the pygame animation loop.  You may have multiple scenes if you wish. Each scene usually
incorporates a level of the game, or some other screen such as an introduction or game summary.

### Constructor
game = simpleGE.Scene(size)  
size is a tuple.  If left out, size is (640, 480)

### Properties
* **screen** - the display surface. An ordinary Pygame surface same size as Scene
* **background** - the background - A pygame surface drawn to screen every frame
* **sprites** - a spriteList (technically an OrderedUpdates) All sprites must be added to this or another list.
  The list can contain sprites and / or tuples containing sprites. Sprites are drawn in the order they appear
  on this list, with later items drawn on top of earlier elements. 
### Standard Methods
* **start()** - begins the animation loop for this scene. Control goes to this scene's event handlers
* **stop()** - ends the animation loop for this scene. Control is reverted to calling function
* **process()** - happens once on every frame. Handy, but *does not* include the formal event handler.
  Overwrite for code you want to execute every frame.
* **doEvents(event)** - is called once for every event in event handler. Overwrite for code that needs access
  to pygame event objects (especially keyboard input)
* **setImage(imageFile, autoSize = True)** - Loads the image into the background of the Scene. If autoSize is
  not listed or set to true, the image will be resized to the Scene's size
* **setCaption(caption)** - sets the caption of this window
* **isKeyPressed(key)** - key should be a pygame keyboard constant. Returns True if that key is currently pressed

### Optional Group Methods
Sprite groups were used to organize groups of sprites, but since the standard sprite list can
contain tuples, the sprite group feature is generally not needed.  It is included for backwards compatibility

* **group = makeSpriteGroup(sprites)** - makes a new sprite group
* **addSpriteGroup(group)** - adds the sprite group to the scene

## Sprite
The sprite class is the workhorse of simpleGE.  It can be used as-is or (more commonly) subclassed to create the 
various elements in your code.  

### Constructor
mySprite = simpleGE.Sprite(scene)  
The scene parameter is the name of the scene that the sprite belongs to
This allows communication between sprites and the scene, and the other sprites

### Inherited Properties
The simpleGE Sprite class is inherited from the pygame Sprite.  So it has access to the pygame.Sprite's two properties:
* **image** - This represents the image to display. It is a pygame Surface object. Normally you will use simpleGE's methods
  manipulate the image, but if you wish to manipulate it directly, you can do so.
* **rect** - the rect is a pygame.Rect object, which represents the size and position of the sprite. You shouldn't need to
  work with this directly, as simpleGE does everything you might need from the rect object.

  In general, you should use the simpleGE techniques first, and if there is something you need that simpleGE cannot do,
  use the image or rect object directly.
  
### Position Properties
* **x** - the x position of the center of the sprite
* **y** - the y position of the center of the sprite
* **left** - the left-hand edge of the sprite
* **right** - the right-hand edge of the sprite
* **top** - the top edge of the sprite
* **bottom** - the bottom edge of the sprite
* **position** - an (x, y) tuple containing the coordinates of the center of the sprite
    
You can get or set any of these elements, but ultimately they all manipulate the x and y values. Other properties
are included for convenience

### Motion Properties 
* **dx** - delta (change) in x every frame.  Positive value moves right, negative value moves left
* **dy** - delta (change in y every frame. Positive value moves down, negative value moves up
* **moveAngle** - indicates an angle of motion every frame
* **speed** - indicates how quickly the sprite moves every frame
* **imageAngle** - indicates how the image is rotated
    
Note that dx and dy control most motion. The other properties are used to calculate dx and dy
for convenience.  Note also that the sprite does not have to be pointed in the motion of travel.

### Status Properties
* **visible** - Boolean. If visible is false, sprite is moved off-screen, no longer responds to collisions or
  boundary checks. Change with hide() and show() methods for best performance.
* **mouseOver** - Boolean.  True if mouse is hovering over this sprite
* **mouseDown** - Boolean. True if mouseOver and mouse button is currently pressed
* **clicked** - Boolean. True if mouse has been clicked and released over this sprite

### Boundary Action Constants
These constants are legal values for the setBoundAction() method.
* **WRAP** - When the sprite leaves the screen, it appears at opposite side
* **BOUNCE** - When the sprite leaves the screen, it bounces off of the edge
* **STOP** - The sprite stops at the screen boundary
* **HIDE** - The sprite's visibility is set to False
* **Continue** - The sprite continues to move off-screen

### Appearance Methods
These methods are used to configure the appearance of the sprite object

* **setImage(imageFile)** - loads imageFile (a valid image in png, gif, or jpg format). For best performance,
  image should be facing to the right, and should not have a lot of extra space around it.
* **copyImage(imageSurface)** - copies a surface as the new sprite image. Normally used with the spritesheet
  class for animation.
* **setSize(width, height)** - sets the size of the image to the expected width and height.
* **colorRect(color, size)** - Sets the sprite to have a particular color and size.  Color is any pygame color
  and size is an (x, y) tuple.  Useful for prototyping if you don't have an image handy.
* **hide()** - make the sprite invisible. Sprite remains in memory, but is moved off-screen and does not respond to
  collisions or boundary checks.
* **show()** - The sprite is made visible. It may be necessary to specify new position and speed.
* **drawTrace(color)** - draws a line from the previous position to the current one

### Motion Methods
These methods (along with the associated propertied) are used to move the sprite.
* **setAngle(angle)** - sets both the imageAngle and moveAngle to the appropriate values. Note angles are in pyGame degree units
* **turnBy(angle)** - turns by the angle amount. Positive angles are counter-clockwise.
* **forward(distance)** - moves distance pixels in the curren image angle direction
* **addForce(amt, angle)** - adds a force vector to the sprite at the speed and angle specified. Used for gravity and other forces

### Event Methods
These methods are used to check the status of the Sprite.
* **process()** - This event is empty by default. In a subclassed Sprite, this event will be called once per frame. The sprite's
  event-handling code will normally go in the process() method.
* **setBoundAction(action)** - Determines what will happen when the sprite attempts to leave the screen. Use the Boundary Action Constants
* **checkBounds()** - Checks the boundary conditions.  Normally this is done for you according to the boundAction you set. But you can
  overwrite this method if you want some other boundary action. You never need to explicitly call this method as it is called automatically
  for each sprite.
* **collidesWith(sprite)** - determines if this sprite is colliding with another sprite. True if collided using AABB method.
* **distanceTo(point)** - determines distance between the center of this sprite and another point (usually position of another sprite or mouse)
* **dirTo(point)** - determines angle between the center of this sprite and another point.
* **isKeyPressed(key)** - key is a pygame keyboard constant.  True if that key is currently pressed.

## GUI Elements
SimpleGE includes a simple but effective GUI system.  GUI elements are also based on the pygame Sprite object, so they should be added to the 
sprite list like other sprites.  However, they are more focused on communication with the user than moving around, so they have different
attributes and methods.

### Label
The label is the basic GUI Element.  It prints text on the screen. It is mainly used for score, time, and other information. It can be used
as-is, or can be subclassed if you want to give it custom behavior. The Label object is designed to present a single line of text.
**Properties**
* **font** - allows you to specify a pygame font object. Default is freesansbold.ttf, which comes with pygame.
* **text** - the text to be rendered.  You can change the text at any time.
* **fgColor** - a pygame color, which will be the color of the rendered text
* **bgColor** - a pygame color, which will be the background if clearBack is False
* **center** - an (x, y) tuple representing the position of the object
* **size** - an (x, y) tuple representing the size of the label. You may need to adjust if you anticipate long text

**Methods**
* **process()** - Overwrite this method in a subclass to give the label some custom behavior
* **hide()** - hide the label
* **show()** - show the label

### Button
The button class is subclassed from the Label, so it has all the same behavior as the label. However, it is intended
as a basic input element, so it has some extra properties used to determine if the user is pressing the button:
* **active** - True if the mouse is currently clicked on the button
* **clicked** - True if the mouse has been clicked and released over the button (this is normally what you want)
 
### TxtInput
 A basic text input field.  Based on the button, so includes all features of Label and Button. Click on the label to start
 input, and then anything typed will be added to the text element. Note that to make this work, you need to call the TxtInput's
 readKeys() method from the Scene's doEvents() method, passing the event object.

* **readKeys()** - if the input element is active (has been clicked,) keyboard input is added to the text element. Use
   backspace to delete the last character and delete to delete the current text.  May not work well with other keyboard
   inputs.

### Scroller
 Based on the Button class, so includes all properties and methods of Button and Label. Used for basic numeric input.
 By default, the scroller displays a numeric value.  Clicking on the left side of the scroller makes the value smaller,
 and clicking on the right side makes it larger.  Additional properties allow you to adjust the behavior of the object:
 * **value** - numeric value
 * **minValue** - smallest allowed value
 * **maxValue** - largest allowed value
 * **increment** - how much the value will change when clicked.

### MultiLabel
 The multilabel is a multi-line label.  It is similar to the Label class, but it includes a list of textLines. It can
 also be clicked like a button. It is most frequently used for game instructions or feedback
 **Properties**
 * **textLines** - a list of strings.  Each element will be a line. Try to make them similar in length for best performance
 * **font** - a pygame Font
 * **fgColor** - foreground color
 * **bgColor** - background color
 * **center** - (x, y) tuple: center of multiLabel
 * **size** - (x, y) tuple: size of multiLabel. You may have to adjust this by hand, as it's hard to predict text size
 * **active** - True if the mouse is currently clicked over this object
 * **clicked** - True if the mouse has been clicked and released over this object
 
 **Methods**
 * **show()** - shows the element
 * **hide()** - hides the element

## Utility Classes
SimpleGame comes with a few other classes to make your life easier as a game programmer.

### Timer
The timer is a basic time element.  You can have as many timers as you want with no performance penalty. 
You can start the timer at any time, and you can get the time since last started. If you want a count-down timer,
You can set the totalTime before you start the timer, and then get the time left. Note that the timer is NOT a 
visual element.  If you want, you can create a label showing the time or time left.

**Properties**
* **totalTime** - how much time is left, used by *getTimeLeft()*

**Methods**
* **start()** - starts or restarts the time
* **getElapsedTime()** - returns time (in seconds) since last started
* **getTimeLeft()** - returns totalTime - elapsed time. Good for countdown timers

### Sound
Pygame sounds are quite easy (if they work at all) but we have also provided a sound class to make it even easier
**Constructor**
mysound = simpleGE.Sound(soundFileName)  

Note that the sound should be in .wav, .ogg, or .mp3 format. You may need to resample using Audacity or the like to get the 
sound to play correctly.

**Methods**
There is only one method:
* **play()** - this plays the current sound one time

Note that the sound object is for sound effects.  For background music,
see the [pygame.mixer.music](https://www.pygame.org/docs/ref/music.html) documentation.

## SpriteSheet

The spritesheet class is a utility to help you manage spritesheets.  These are images with several sub-images.  Often
they are used for tiles in a tile map or in character animation.  Download the spritesheet image you want into your 
working directory, and this class can help you extract the images you need for your own animations.  You can have more
than one SpriteSheet class working with the same spritesheet image if you wish. It is often useful to examine the spritesheet
image in an image editor like Gimp or Krita so you can see how large the images are and where they are located.

**Constructor**  
The constructor is a bit complex, as the spritesheet only works when it knows a fair amount about the image it is working with:  
walkAnim = SpriteSheet(imageFile, cellSize, numRows, numCols, delay)  

All of the parameters are attributes that can be changed.  
* **imageFile** - the file name of the spritesheet image
* **cellSize** - an (x, y) tuple containing the size of a single sub-image.  This is usually a power of two, like (32, 32) or (64, 64)
* **numRows** - if you are working with an animation, you are normally interested in several rows of images.
  This parameter describes how many rows in the animation. Normally each row will describe a different direction
* **numCols** - This parameter describes how many columns, which is normally the number of frames in the animation cycle
* **delay** - This parameter indicates the delay (in seconds) between showing frames.  You can adjust this to specify the speed of
  the animation. If you skip this parameter, it will be .1.

If your spritesheet image contains only one animation (say a walk cycle going in four directions) this is all you need.  However,
many spritesheets contain multiple animations, so you can change the offset property to indicate where a particular animation begins

**Properties** 
All of the parameters of the constructor, plus:
* **timer** - a simpleGE timer. It is used automatically to manage the delay, so you shouldn't need to mess with it
* **offset** - an (x, y) coordinate pair indicating the upper left corner (in pixels) of the current animation.  Useful when a spritesheet
  image contains multiple animations.
* **animImage** - the entire spritesheet animation.  It will be used automatically, so you shouldn't need to do anything with it.) h
* **startCol** - this indicates the position of the first cell of the animation. Normally this is zero, but some spritesheets (specifically
  those from the popular liberated pixel cup series) have an idle animation on cell zero, so in this case set startCol to 1.
* **animRow** - Current row of the animation.
* **animCol** - Current column of the animation. 

**Methods**
* **getCellImage(row, col)** - returns a single pygame Surface representing the image at a particular cell row and column. Use the sprite's
  copyImage() method to copy this image to your current sprite.  GetCellImage is usually used for extracting a single cell, like in a tile map.
  Row and column are cell values counted from the offset, not pixels.
* **getNext(self, animRow)** - returns the next image in the current row. Returs a pygame Surface representing the next image of the current row.in
  This automatically cycles back to the startCol, so the animation will continue. Use the Sprite's copyImage() method to use this Surface.
