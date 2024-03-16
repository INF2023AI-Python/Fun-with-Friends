import os
import pygame
from pygame.locals import *
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# This makes it so that gamepad input can be used even if the window is not in focus
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = 0

# Matrix & Canvas
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for available gamepads
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No gamepads detected. Exiting.")

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

# Setup screen
screen_width, screen_height = 32, 32
screen = pygame.display.set_mode((screen_width * 2, screen_height))
pygame.display.set_caption("Game Template")

# Game variables
player_pos_x, player_pos_y = 16, 16

# Additional variables (self-explanatory)
clock = pygame.time.Clock()
enable_input = True

run = True
while run:
    # Player Physics
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE and enable_input:
            print("Spacebar pressed")
        elif event.type == pygame.JOYBUTTONDOWN and enable_input:
            button = event.button
            print(f"Button {button} pressed")

    # Drawing
    offset_canvas.Clear()
    offset_canvas.SetPixel(player_pos_x, player_pos_y, 255, 255, 255)
    offset_canvas = matrix.SwapOnVSync(offset_canvas)

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
