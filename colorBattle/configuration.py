#import time
#import board #access to the hardware on your board
#import rgbmatrix #access that hardware as inputs/outputs
#import digitalio #control the flow of your code in multiple ways, including passing time by 'sleeping'.
#probably using pygame for handling events, pygame has a built-in pygame.joystick module
#import evdev #dont need evdev anymore (for the gamepad, when using pygame,


import pygame #simplifies the process of handling events, managing graphics, and organizing game logic
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions


#Configuration for Matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options = options)

# Set up gamepads, this is using endev, need to change it to pygame
#gamepad1 = evdev.InputDevice('/dev/input/eventX')  # Replace 'X' with the event number for gamepad 1 #ls /dev/input/
#gamepad2 = evdev.InputDevice('/dev/input/eventY')  # Replace 'Y' with the event number for gamepad 2

#----------------------------------------------------------------------------------------------------
# Initialize Pygame
pygame.init()

#set up display
width, height = 32, 32  # LED matrix dimensions
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Color Battle")
# Set up Pygame screen
#? screen = pygame.display.set_mode((options.cols, options.rows))

#initialize joystick
pygame.joystick.init()
#check for available gamepads
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

if not joysticks:
    print("No gamepads detected. Exiting.")
    pygame.quit()
    sys.exit()

joysticks[0].init()
joysticks[1].init()

#----------------------------------------------------------------------------------------------------

#Main game loop
running = True
clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle gamepad input
    for i in range(2):  # Assuming two gamepads
        joystick = joysticks[i]

        # Get input from the gamepad
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)


################################# Game Code ###################################

    # flip() the display to put your work on screen
    #pygame.display.flip()

    # Convert pygame surface to RGBMatrix format
    pygame.surfarray.blit_array(matrix, pygame.surfarray.array3d(screen))

    # Refresh display
    matrix.UpdateScreen()

    #cap the frame rate
    clock.tick(60)
    
pygame.quit()
sys.exit()