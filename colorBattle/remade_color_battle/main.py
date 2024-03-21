# Import necessary modules
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pygame
from obstacle import obstacle, maze
from scoreboard import Scoreboard
from levelSelection import select_level
from player import Player
from controllers import controllers

# Constants and Configurations
PLAY_HEIGHT = 26
PLAY_WIDTH = 32
GAME_DURATION = 60

# Initialize RGB Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Initialize Pygame
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Initialize Players
player1 = Player((255, 255, 0), (255, 0, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 - 10))
player2 = Player((0, 0, 255), (0, 255, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 + 10))

# Initialize Scoreboard
scoreboard = Scoreboard(offset_canvas)

grid = [[(0, 0, 0) for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]

# Initialize Game Area
game_area = obstacle(offset_canvas, matrix)
maze_pattern = maze(offset_canvas, matrix)

def count_points(grid, color1, color2):
    player1_points = sum(row.count(color1) for row in grid)
    player2_points = sum(row.count(color2) for row in grid)
    return player1_points, player2_points

def main():
    running = True
    clock = pygame.time.Clock()

    # Your original code for selecting the level
    # select_level(matrix, offset_canvas, joysticks)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Your original code for player controls
        # controllers(joysticks, player1, player2, maze_pattern, game_area)

        # Painting
        player1.paint(offset_canvas)
        player2.paint(offset_canvas)

        player1.update_state(grid)
        player2.update_state(grid)

        # Count points and determine the winner
        player1_points, player2_points = count_points(grid, player1.color, player2.color)

        # Draw scoreboard
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION, player1_points, player2_points)

        # Check if remaining time is zero
        if remaining_seconds == 0:
            running = False

        # Swap and delay
        matrix.SwapOnVSync(offset_canvas)
        clock.tick(300)

    pygame.quit()

if __name__ == "__main__":
    main()
