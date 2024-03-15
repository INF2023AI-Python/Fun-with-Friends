import pygame
from player import Player, PLAY_WIDTH, PLAY_HEIGHT
from emulator import Emulator
from controllers import controllers
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def count_points(grid, player1_color, player2_color):
    player1_points = sum(row.count(player1_color) for row in grid)  # Count cells occupied by player 1
    player2_points = sum(row.count(player2_color) for row in grid)  # Count cells occupied by player 2

    return player1_points, player2_points


def run_game():
    # Initialize Pygame
    pygame.init()

    # Initialize the gamepad controllers
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    # Initialize the players
    player1 = Player((255, 0, 0), (0, 0))  # Red player starting at (0, 0)
    player2 = Player((0, 255, 0), (31, 31))  # Green player starting at (31, 31)

    # Initialize the game grid
    grid = [[(0, 0, 0) for _ in range(PLAY_HEIGHT)] for _ in range(PLAY_WIDTH)]

    # Initialize the emulator
    emulator = Emulator(PLAY_WIDTH, PLAY_HEIGHT)

    # Initialize the game area and maze pattern
    game_area = [[0 for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]
    maze_pattern = obstacle(game_area, emulator.matrix)  # You need to modify your 'obstacle' function to return the maze pattern

    # Get the start time
    start_ticks = pygame.time.get_ticks()

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if 60 seconds have passed
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > 60:  # if more than 60 seconds close the game
            break

        # Player controls
        controllers(joysticks, player1, player2, maze_pattern, game_area)  # You need to modify your 'controllers' function to accept 'maze_pattern' and 'game_area' as arguments

        # Painting
        player1.paint(grid)
        player2.paint(grid)

        # Update the display
        emulator.update_canvas(grid)

        # Frame rate (e.g., 60 FPS)
        pygame.time.delay(int(1000 / 60))

    # Count points and determine the winner
    player1_points, player2_points = count_points(grid, player1.color, player2.color)
    if player1_points == player2_points:
        print("It's a tie!")
    elif player1_points > player2_points:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")

    # Quit Pygame
    pygame.quit()



if __name__ == "__main__":
    run_game()
