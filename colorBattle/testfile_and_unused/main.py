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

# Initialize Scoreboard
scoreboard = Scoreboard(offset_canvas)

# Initialize Game Area
game_area = obstacle(offset_canvas, matrix)
maze_pattern = maze(offset_canvas, matrix)

# Define the grid to save the points
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
        self.button_up_pressed = False
        self.button_right_pressed = False
        self.button_down_pressed = False
        self.button_left_pressed = False
        self.speed = 3

    def move(self, grid, canvas):
        # get current postion
        x = self.position[0]
        y = self.position[1]
        
        # calculate the amount of position change
        dx = round(self.x_axis * self.speed)
        dy = round(self.y_axis * self.speed)

        # new position
        if not is_collision(new_x, new_y):
            new_x = (x + dx) % PLAY_WIDTH
            new_y = (y + dy) % PLAY_HEIGHT

        # wrap the player in play field
        new_x = new_x if new_x >= 0 else PLAY_WIDTH + new_x
        new_y = new_y if new_y >= 0 else PLAY_HEIGHT + new_y

        # gradually update position for smooth movement, to make it look like it move one pixel by one pixel
        steps = max(abs(dx), abs(dy))
        for i in range(steps):
            interp_x = round(x + (dx * i) / steps)
            interp_y = round(y + (dy * i) / steps)
            if 0 <= interp_x < PLAY_WIDTH and 0 <= interp_y < PLAY_HEIGHT:
                grid[interp_y][interp_x] = self.trail_color #leave the trail of the player
                canvas.SetPixel(interp_x, interp_y, *self.trail_color)
            pygame.time.delay(5)  # a small delay for smooth movement
        
        # update position
        self.position = (new_x, new_y)

    def paint(self, canvas):
        # paint the postion of the player
        canvas.SetPixel(self.position[0], self.position[1], *self.trail_color)

    def update_state(self, grid):
        x, y = self.position
        grid[y][x] = self.trail_color

    def is_collision(self, x, y, maze_pattern, game_area):
        # collision check, it ought to be added in move function, to make sure the player will not cross the barriers
        # PROBLEM: if add is_collision, player movement will be more worse
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

    # selecting the level
    select_level(matrix, offset_canvas, joysticks)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                for i, _ in enumerate(joysticks):
                    # check get pressed 
                    if i == 0:  # Player 1 controls
                        if event.button == 0:  # Button 0 (Up)
                            player1.button_up_pressed = True
                        elif event.button == 1:  # Button 1 (Right)
                            player1.button_right_pressed = True
                        elif event.button == 2:  # Button 2 (Down)
                            player1.button_down_pressed = True
                        elif event.button == 3:  # Button 3 (Left)
                            player1.button_left_pressed = True
                    elif i == 1:  # Player 2 controls
                        if event.button == 0:  # Button 0 (Up)
                            player2.button_up_pressed = True
                        elif event.button == 1:  # Button 1 (Right)
                            player2.button_right_pressed = True
                        elif event.button == 2:  # Button 2 (Down)
                            player2.button_down_pressed = True
                        elif event.button == 3:  # Button 3 (Left)
                            player2.button_left_pressed = True
            elif event.type == pygame.JOYBUTTONUP:
                for i, _ in enumerate(joysticks):
                    # check button realse
                    if i == 0:  # Player 1 controls
                        if event.button == 0:  # Button 0 (Up)
                            player1.button_up_pressed = False
                        elif event.button == 1:  # Button 1 (Right)
                            player1.button_right_pressed = False
                        elif event.button == 2:  # Button 2 (Down)
                            player1.button_down_pressed = False
                        elif event.button == 3:  # Button 3 (Left)
                            player1.button_left_pressed = False
                    elif i == 1:  # Player 2 controls
                        if event.button == 0:  # Button 0 (Up)
                            player2.button_up_pressed = False
                        elif event.button == 1:  # Button 1 (Right)
                            player2.button_right_pressed = False
                        elif event.button == 2:  # Button 2 (Down)
                            player2.button_down_pressed = False
                        elif event.button == 3:  # Button 3 (Left)
                            player2.button_left_pressed = False

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
        clock.tick(300)

    pygame.quit()

if __name__ == "__main__":
    main()