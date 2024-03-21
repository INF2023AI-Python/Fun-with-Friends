from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import os
from player import Player
from controllers import controllers
from obstacle import obstacle, maze
from levelSelection import select_level
from scoreboard import Scoreboard

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 26
GAME_DURATION = 60

# Initialize RGBMatrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

def main():
    # Initialise Pygame
    pygame.init()
    os.environ["XDG_RUNTIME_DIR"] = "/tmp"
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Initialize the game grid
    grid = [[(0, 0, 0) for _ in range(PLAY_HEIGHT)] for _ in range(PLAY_WIDTH)]

    # Initialize players
    player1 = Player((255, 255, 0), (255, 0, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 - 10))
    player2 = Player((0, 0, 255), (0, 255, 0), (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 + 10))

    # Create an instance for scoreboard
    scoreboard = Scoreboard(offset_canvas, player1, player2)

    # Easy mode
    game_area = obstacle(offset_canvas, matrix)

    # Hard mode: maze
    maze_pattern = maze(offset_canvas, matrix)

    remaining_seconds = GAME_DURATION

    running = True
    clock = pygame.time.Clock()

    # select the level, easy or hard
    # select_level(matrix, offset_canvas, joysticks)
    obstacle(offset_canvas, matrix)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls
        controllers(joysticks, player1, player2, maze_pattern, game_area)
        
        # Painting
        player1.paint(offset_canvas)
        player2.paint(offset_canvas)

        # Count points and determine the winner
        player1.update_state(grid)
        player2.update_state(grid)
        
        if player1.cells_painted == player2.cells_painted:
            print("It's a tie!")
        elif player1.cells_painted > player2.cells_painted:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")

        # Draw the updated scoreboard
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION)

        # Check if remaining time is zero
        if remaining_seconds == 0:
            running = False

        clock.tick(60)
        # Update the display
        matrix.SwapOnVSync(offset_canvas)

    # Game over, quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
