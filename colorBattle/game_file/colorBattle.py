# Import necessary modules
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import pygame
from obstacle import obstacle, maze
from scoreboard import Scoreboard, count_points
from levelSelection import select_level
from movement import Player
from endPage import display_text, winner

# Constants and Configurations
PLAY_HEIGHT = 26 # 6x32 will be left for the scoreboard 
PLAY_WIDTH = 32
GAME_DURATION = 10

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



def main():
    running = True
    clock = pygame.time.Clock()

    player1 = Player(player1_color, player1_trail_color, player1_start_pos)
    player2 = Player(player2_color, player2_trail_color, player2_start_pos)

    # Problem in selecting the level: if applied muss check Collision! but check collsion causes Problem in movement 
    level = select_level(matrix, offset_canvas, joysticks)
    if level == "hard":
        maze(offset_canvas, matrix)
    if level == "easy":
        obstacle(offset_canvas, matrix)
    
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
                            if -0.2 < player1.x_axis < 0.2 and player1.y_axis < -0.8:
                                player1.y_axis = -1  # Move up
                            elif -0.2 < player1.x_axis < 0.2 and player1.y_axis > 0.8:
                                player1.y_axis = 1  # Move down
                            elif player1.x_axis > 0.8 and -0.2 < player1.y_axis < 0.2:
                                player1.x_axis = 1  # Move right
                            elif player1.x_axis < -0.8 and -0.2 < player1.y_axis < 0.2:
                                player1.x_axis = -1  # Move left
                            print("Player 1 - X Axis:", player1.x_axis, "Y Axis:", player1.y_axis)
                        elif i == 1:  # Player 2 controls
                            player2.x_axis = joystick.get_axis(0)
                            player2.y_axis = joystick.get_axis(1)
                            if -0.2 < player2.x_axis < 0.2 and player2.y_axis < -0.8:
                                player2.y_axis = -1  # Move up
                            elif -0.2 < player2.x_axis < 0.2 and player2.y_axis > 0.8:
                                player2.y_axis = 1  # Move down
                            elif player2.x_axis > 0.8 and -0.2 < player2.y_axis < 0.2:
                                player2.x_axis = 1  # Move right
                            elif player2.x_axis < -0.8 and -0.2 < player2.y_axis < 0.2:
                                player2.x_axis = -1  # Move left
                            print("Player 2 - X Axis:", player2.x_axis, "Y Axis:", player2.y_axis)


        player1.move(level, grid, offset_canvas)
        player2.move(level, grid, offset_canvas)

        player1.paint(offset_canvas)
        player2.paint(offset_canvas)
        
        player1_points, player2_points = count_points(grid, player1_trail_color, player2_trail_color)

        # Draw scoreboard
        remaining_seconds = scoreboard.draw(offset_canvas, GAME_DURATION, player1_points, player2_points)

        # Check if remaining time is zero, if zero end the game loop
        if remaining_seconds == 0:
            running = False

        # Swap and delay
        matrix.SwapOnVSync(offset_canvas)
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
    #show who wins after game finish
    player1_points, player2_points = count_points(grid, player1_trail_color, player2_trail_color)
    result = winner(player1_points, player2_points)
    matrix.Clear()
    display_text(result, (255, 255, 0), offset_canvas, matrix)
    time.sleep(5)