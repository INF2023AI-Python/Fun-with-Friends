# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions
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
scoreboard = Scoreboard(offset_canvas)

# Easy mode
game_area = obstacle(offset_canvas, matrix)
# Hard mode: maze
maze_pattern = maze(offset_canvas, matrix)

remaining_seconds = GAME_DURATION


def main():
    running = True
    clock = pygame.time.Clock()

    # select the level, easy or hard
    # select_level(matrix, offset_canvas, joysticks)
    obstacle(offset_canvas, matrix)
    # maze(offset_canvas, matrix)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                if button == 0:  # Up button
                    player1.move('UP', maze_pattern, game_area)
                elif button == 1:  # Right button
                    player1.move('RIGHT', maze_pattern, game_area)
                elif button == 2:  # Down button
                    player1.move('DOWN', maze_pattern, game_area)
                elif button == 3:  # Left button
                    player1.move('LEFT', maze_pattern, game_area)

        # Painting
        player1.paint(offset_canvas)
        player2.paint(offset_canvas)

        player1.update_state(grid)
        player2.update_state(grid)

        # Count points and determine the winner
        player1_points, player2_points = count_points(grid, player1.color, player2.color)
        if player1_points == player2_points:
            print("It's a tie!")
        elif player1_points > player2_points:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")

        # Draw the updated scoreboard
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION, player1_points, player2_points)

        # Check if remaining time is zero
        if remaining_seconds == 0:
            running = False

        clock.tick(30)  # Adjust frame rate as needed
        matrix.SwapOnVSync(offset_canvas)

    pygame.quit()


def count_points(grid, player1_color, player2_color):
    player1_points = sum(row.count(player1_color) for row in grid)  # Count cells occupied by player 1
    player2_points = sum(row.count(player2_color) for row in grid)  # Count cells occupied by player 2
    print(player1_points)
    print(player2_points)
    return player1_points, player2_points

if __name__ == "__main__":
    main()