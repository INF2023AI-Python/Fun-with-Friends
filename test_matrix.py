import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Initialize Pygame
pygame.init()

# Set up Pygame screen
width, height = 32, 32  # Adjust according to your RGB matrix dimensions
screen = pygame.display.set_mode((width, height))

# Configure RGB matrix
options = RGBMatrixOptions()
options.rows = height
options.cols = width
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options=options)

# Player variables
player_size = 4
player_x, player_y = width // 2, height // 2
player_speed = 1

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get input from the gamepad
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    axis_x = joystick.get_axis(0)
    axis_y = joystick.get_axis(1)

    # Update player position based on gamepad input
    player_x += int(axis_x * player_speed)
    player_y += int(axis_y * player_speed)

    # Draw
    screen.fill((0, 0, 0))  # Clear the screen

    # Draw player
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, player_size, player_size))

    # Convert Pygame surface to RGBMatrix format
    pygame.surfarray.blit_array(matrix, pygame.surfarray.array3d(screen))

    # Refresh display
    matrix.SwapOnVSync()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
