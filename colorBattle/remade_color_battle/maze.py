from rgbmatrix import RGBMatrix, RGBMatrixOptions
from scoreboard import Scoreboard
import pygame
import random

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

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize Scoreboard
scoreboard = Scoreboard(offset_canvas)


class Player:
    def __init__(self, color, trail_color, start_pos):
        self.color = color
        self.trail_color = trail_color
        self.position = start_pos
        self.x_axis = 0
        self.y_axis = 0
        self.speed = 2

    def move(self, maze, canvas):
        # 获取当前位置
        x = self.position[0]
        y = self.position[1]

        # 计算位置变化量
        dx = round(self.x_axis * self.speed)
        dy = round(self.y_axis * self.speed)

        # 更新新位置
        new_x = (x + dx) % PLAY_WIDTH
        new_y = (y + dy) % PLAY_HEIGHT

        # 调整新位置以在游戏区域内移动
        new_x = new_x if new_x >= 0 else PLAY_WIDTH + new_x
        new_y = new_y if new_y >= 0 else PLAY_HEIGHT + new_y

        # 检查新位置是否为墙，如果是墙则停止移动
        if maze[new_y][new_x] != '#':
            # 逐渐更新位置，实现顺滑移动
            steps = max(abs(dx), abs(dy))
            for i in range(steps):
                interp_x = round(x + (dx * i) / steps)
                interp_y = round(y + (dy * i) / steps)
                if 0 <= interp_x < PLAY_WIDTH and 0 <= interp_y < PLAY_HEIGHT:
                    canvas.SetPixel(interp_x, interp_y, *self.trail_color)
            # 更新当前位置
            self.position = (new_x, new_y)

    def paint(self, canvas):
        canvas.SetPixel(self.position[0], self.position[1], *self.color)

class MazeGame:
    def __init__(self):
        self.maze1, self.start1, self.end1 = self.generate_maze(PLAY_HEIGHT // 2, PLAY_WIDTH)
        self.maze2, self.start2, self.end2 = self.generate_maze(PLAY_HEIGHT // 2, PLAY_WIDTH)

        self.player1 = Player(YELLOW, GREEN, self.start1)
        self.player2 = Player(BLUE, WHITE, self.start2)

    def generate_maze(self, height, width):
        maze = [['#'] * width for _ in range(height)]  # Initialize maze with walls

        # Randomly generate starting point and ending point
        start_row, start_col = random.randint(0, height - 1), random.randint(0, width - 1)
        end_row, end_col = random.randint(0, height - 1), random.randint(0, width - 1)

        # Set starting point and ending point as passage
        maze[start_row][start_col] = 'S'
        maze[end_row][end_col] = 'E'

        # Generate maze recursively
        self.generate_maze_recursive(maze, start_row, start_col)

        return maze, (start_row, start_col), (end_row, end_col)

    def generate_maze_recursive(self, maze, row, col):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Up, Down, Left, Right
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == '#':
                maze[new_row][new_col] = ' '  # Set the cell as passage
                maze[row + dr // 2][col + dc // 2] = ' '  # Break the wall between the cells
                self.generate_maze_recursive(maze, new_row, new_col)

    def draw_maze(self, canvas, maze):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == '#':
                    canvas.SetPixel(col, row, *BLACK)  # Draw wall
                elif maze[row][col] == 'S':
                    canvas.SetPixel(col, row, *YELLOW)  # Draw start point
                elif maze[row][col] == 'E':
                    canvas.SetPixel(col, row, *BLUE)  # Draw end point
                else:
                    canvas.SetPixel(col, row, *WHITE)  # Draw passage

    def move_players(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        for i, joystick in enumerate(joysticks):
            if i == 0:  # Player 1 controls
                self.player1.x_axis = joystick.get_axis(0)
                self.player1.y_axis = joystick.get_axis(1)
            elif i == 1:  # Player 2 controls
                self.player2.x_axis = joystick.get_axis(0)
                self.player2.y_axis = joystick.get_axis(1)

        self.player1.move(self.maze1, offset_canvas)
        self.player2.move(self.maze2, offset_canvas)

        return True

    def check_game_status(self):
        if self.player1.position == self.end1:
            return "Player 1 wins!"
        elif self.player2.position == self.end2:
           
             return "Player 2 wins!"
        else:
            return None

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.move_players()
            self.draw_maze(offset_canvas, self.maze1)
            self.draw_maze(offset_canvas, self.maze2)
            self.player1.paint(offset_canvas)
            self.player2.paint(offset_canvas)

            game_status = self.check_game_status()
            if game_status:
                print(game_status)
                break

            matrix.SwapOnVSync()

            clock.tick(30)  # 控制帧率

if __name__ == "__main__":
    game = MazeGame()
    game.main()