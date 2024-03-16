#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import obstacle
from scoreboard import Scoreboard
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

scoreboard = Scoreboard(offset_canvas)

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

        # Update the scoreboard
        scoreboard.update(GAME_DURATION)

        # Draw the updated scoreboard
        scoreboard.draw()

        clock.tick(120)
        # Update the display
        matrix.SwapOnVSync(offset_canvas)

        # Delay to control frame rate
        # pygame.time.delay(1000)  # Delay for 1 second (1000 milliseconds)

    pygame.quit()

if __name__ == "__main__":
    main()