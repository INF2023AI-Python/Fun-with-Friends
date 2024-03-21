# Import necessary modules
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pygame
from obstacle import obstacle, maze
from scoreboard import Scoreboard
from levelSelection import select_level

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
for i, joystick in enumerate(joysticks):
    axis_x = joystick.get_axis(0)
    axis_y = joystick.get_axis(1)

# Initialize Scoreboard
scoreboard = Scoreboard(offset_canvas)

# Initialize Game Area
game_area = obstacle(offset_canvas, matrix)
maze_pattern = maze(offset_canvas, matrix)

# Define the grid
grid = [[(0, 0, 0) for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]

# Initialize Players
player1_color = (255, 255, 0)
player1_trail_color = (255, 0, 0)
player1_start_pos = (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 - 10)
player1_position = player1_start_pos
player1_trail = [player1_start_pos]
player1_cells_painted = 0

player2_color = (0, 0, 255)
player2_trail_color = (0, 255, 0)
player2_start_pos = (PLAY_HEIGHT // 2, PLAY_WIDTH // 2 + 10)
player2_position = player2_start_pos
player2_trail = [player2_start_pos]
player2_cells_painted = 0

def move_player(position, x_axis, y_axis, maze_pattern, game_area):
    x, y = position
    new_x, new_y = x, y

    # Adjust the position based on gamepad input
    if abs(x_axis) > 0.5:
        new_x = (x + int(x_axis)) % PLAY_WIDTH
    if abs(y_axis) > 0.5:
        new_y = (y + int(y_axis)) % PLAY_HEIGHT

    if not is_collision(new_y, new_x, maze_pattern, game_area):
        position = (new_x, new_y)
        return position

def paint_player(canvas, position, trail_color):
    # Check if the indices are within the range of the grid dimensions
    x, y = position
    canvas.SetPixel(x, y, *trail_color)

def update_state(grid, position, trail_color):
    # Update the game state based on the player's position and color
    x, y = position
    if y < len(grid) and x < len(grid[0]):
        grid[y][x] = trail_color

def is_collision(y, x, maze_pattern, game_area):
    # Check if the indices are within the range of the grid dimensions
    if y < len(maze_pattern) and x < len(maze_pattern[0]):
        if maze_pattern[y][x] == "#":
            return True
        if game_area[y][x] == 1:
            return True
    return False

def count_points(grid, color1, color2):
    player1_points = sum(row.count(color1) for row in grid)
    player2_points = sum(row.count(color2) for row in grid)
    return player1_points, player2_points

def main():
    running = True
    clock = pygame.time.Clock()

    # Your original code for selecting the level
    select_level(matrix, offset_canvas, joysticks)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Your original code for player controls
        for joystick in joysticks:
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)

            player1_position = move_player(player1_position, x_axis, y_axis, maze_pattern, game_area)
            player2_position = move_player(player2_position, x_axis, y_axis, maze_pattern, game_area)

        # Painting
        paint_player(offset_canvas, player1_position, player1_trail_color)
        paint_player(offset_canvas, player2_position, player2_trail_color)

        update_state(grid, player1_position, player1_trail_color)
        update_state(grid, player2_position, player2_trail_color)
        
        player1_points, player2_points = count_points(grid, player1_trail_color, player2_trail_color)

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
