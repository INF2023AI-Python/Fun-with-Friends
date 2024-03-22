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

class Player:
    def __init__(self, color, trail_color, start_pos):
        self.color = color
        self.trail_color = trail_color
        self.position = start_pos
        self.x_axis = 0
        self.y_axis = 0

    def move(self, maze_pattern, game_area):
    # 根据方向键的轴值移动一个像素
        new_x = (self.position[0] + round(self.x_axis * 1)) % PLAY_WIDTH
        new_y = (self.position[1] + round(self.y_axis * 1)) % PLAY_HEIGHT
        if not self.is_collision(new_x, new_y, maze_pattern, game_area):
            self.position = (new_x, new_y)

    def paint(self, canvas):
        canvas.SetPixel(self.position[0], self.position[1], *self.trail_color)

    def update_state(self, grid):
        x, y = self.position
        grid[y][x] = self.trail_color


    def is_collision(self, x, y, maze_pattern, game_area):
        if maze_pattern[y][x] == "#" or game_area[y][x] == 1:
            return True
        return False

def count_points(grid, color1, color2):
    player1_points = sum(row.count(color1) for row in grid)
    player2_points = sum(row.count(color2) for row in grid)
    return player1_points, player2_points

def main():
    running = True
    clock = pygame.time.Clock()

    player1 = Player((255, 255, 0), (255, 0, 0), (PLAY_WIDTH // 2 - 10, PLAY_HEIGHT // 2))
    player2 = Player((0, 0, 255), (0, 255, 0), (PLAY_WIDTH // 2 + 10, PLAY_HEIGHT // 2))

    # Your original code for selecting the level
    select_level(matrix, offset_canvas, joysticks)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # joysticks movement
            if event.type == pygame.JOYAXISMOTION:
                    for i, joystick in enumerate(joysticks):
                        if i == 0:  # Player 1 controls
                            player1.x_axis = joystick.get_axis(0)
                            player1.y_axis = joystick.get_axis(1)
                            print("Player 1 - X Axis:", player1.x_axis, "Y Axis:", player1.y_axis)
                        elif i == 1:  # Player 2 controls
                            player2.x_axis = joystick.get_axis(0)
                            player2.y_axis = joystick.get_axis(1)
                            print("Player 2 - X Axis:", player2.x_axis, "Y Axis:", player2.y_axis)


        player1.move(maze_pattern, game_area)
        player2.move(maze_pattern, game_area)

        player1.paint(offset_canvas)
        player2.paint(offset_canvas)

        player1.update_state(grid)
        player2.update_state(grid)
        
        player1_points, player2_points = count_points(grid, player1_trail_color, player2_trail_color)

        # Draw scoreboard
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION, player1_points, player2_points)

        # Check if remaining time is zero
        if remaining_seconds == 0:
            running = False

        # Swap and delay
        matrix.SwapOnVSync(offset_canvas)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
