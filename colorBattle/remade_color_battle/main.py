# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
# from obstacle import obstacle, maze
from scoreboard import Scoreboard
from levelSelection import select_level
from game_loop import run_game
# from game_loop import player1_points, player2_points
#pip install numpy

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 26
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

#create a instance for scoreboard
scoreboard = Scoreboard(offset_canvas)

def main():
    running = True
    clock = pygame.time.Clock()

    #select rhe level, easy or hard

    select_level(matrix, offset_canvas, joysticks)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # run_game()

        # Update the scoreboard
        scoreboard.update(GAME_DURATION)

        # Draw the updated scoreboard, NEED TO MAKE SURE DRAW ON THE SAME CANVAS
        scoreboard.draw(offset_canvas)


        clock.tick(300)
        # Update the display
        matrix.SwapOnVSync(offset_canvas)

        # Delay to control frame rate
        # pygame.time.delay(1000)  # Delay for 1 second (1000 milliseconds)

    pygame.quit()

if __name__ == "__main__":
    main()