# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
from obstacle import obstacle, maze
from scoreboard import Scoreboard
from levelSelection import select_level
from player import Player
from controllers import controllers
import os

# from game_loop import player1_points, player2_points
# pip install numpy

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 26

#set duration
GAME_DURATION = 60

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Initialise
pygame.init()
os.environ["XDG_RUNTIME_DIR"] = "/path/to/runtime/directory"
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Initialize the game grid
grid = [[(0, 0, 0) for _ in range(PLAY_HEIGHT)] for _ in range(PLAY_WIDTH)]

pygame.display.set_caption("Color Battle")

# initialize players
player1 = Player((255, 255, 0), (255, 0, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 - 10))
player2 = Player((0, 0, 255), (0, 255, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 + 10))
# create an instance for scoreboard
scoreboard = Scoreboard(offset_canvas, player1, player2)

# Easy mode
game_area = obstacle(offset_canvas, matrix)
# Hard mode: maze
maze_pattern = maze(offset_canvas, matrix)

remaining_seconds = GAME_DURATION


def main():
    running = True
    clock = pygame.time.Clock()

    # select the level, easy or hard
    select_level(matrix, offset_canvas, joysticks)
    # obstacle(offset_canvas, matrix)
    # maze(offset_canvas, matrix)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        controllers(joysticks, player1, player2, maze_pattern, game_area)
        # Painting
        player1.paint(offset_canvas)
        player2.paint(offset_canvas)

        player1.update_state(grid)
        player2.update_state(grid)

        # Count points and determine the winner
        # player1_points, player2_points = count_points(grid, player1.color, player2.color)
        # print(f"{player1_points} and {player2_points}")
        if player1.cells_painted == player2.cells_painted:
            print("It's a tie!")
        elif player1.cells_painted > player2.cells_painted:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")

        # Draw the updated scoreboard, NEED TO MAKE SURE DRAW ON THE SAME CANVAS
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION, player1, player2)

        # Check if remaining time is zero
        if remaining_seconds == 0:
            running = False

        clock.tick(300)
        # Update the display
        matrix.SwapOnVSync(offset_canvas)
        # Delay to control frame rate
        # pygame.time.delay(1000)  # Delay for 1 second (1000 milliseconds)

    # Game over, quit Pygame
    pygame.quit()


# def count_points(grid, player1_color, player2_color):
#     player1_points = sum(row.count(player1_color) for row in grid)  # Count cells occupied by player 1
#     player2_points = sum(row.count(player2_color) for row in grid)  # Count cells occupied by player 2
#     print(player1_points)
#     print(player2_points)
#     return player1_points, player2_points

if __name__ == "__main__":
    main()
