#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pygame
import obstacle  # Import the obstacle module
#pip install numpy

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
GAME_DURATION = 60

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

pygame.display.set_caption("Color Battle")

# Initialise
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

def main():
    running = True
    clock = pygame.time.Clock()
    # Draw obstacle
        # Easy mode
    #obstacle.obstacle(offset_canvas, matrix)
        # Hard mode: maze
    obstacle.maze(offset_canvas, matrix)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Read input, keep players in the area
        # wrapping()
        # input(joysticks)

        

        clock.tick(60)
        matrix.SwapOnVSync(offset_canvas)

    pygame.quit()

if __name__ == "__main__":
    main()