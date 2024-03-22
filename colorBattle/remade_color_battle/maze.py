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
    # Class attributes for colors
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    def __init__(self, start_pos, color):
        self.position = start_pos
        self.x_axis = 0
        self.y_axis = 0
        self.speed = 2
        self.color = color

    def move(self, maze):
        # 获取当前位置
        x = self.position[0]
        y = self.position[1]

        # 计算位置变化量
        dx = round(self.x_axis * self.speed)
        dy = round(self.y_axis * self.speed)

        # 更新新位置
        new_x = (x + dx) % PLAY_WIDTH
        new_y = (y + dy) % PLAY_HEIGHT

        # 检查新位置是否为墙，如果是墙则停止移动
        if maze[new_y][new_x] != '#':
            # 更新当前位置
            self.position = (new_x, new_y)

    # 绘制玩家
    def paint(self, canvas):
        # 根据当前对象的类别选择颜色
        if self.__class__ == Player:
            color = Player.YELLOW  # 默认为黄色
        else:
            color = self.__class__.color

        canvas.SetPixel(self.position[0], self.position[1], *color)

class MazeGame:
    def __init__(self):
        # Define colors for each player
        self.player1_color = Player.GREEN
        self.player2_color = Player.BLUE

        self.player1 = Player((0, 0), GREEN)
        self.player2 = Player((PLAY_WIDTH - 1, PLAY_HEIGHT - 1), BLUE)

        # Generate mazes
        self.maze1 = self.generate_maze(PLAY_HEIGHT, PLAY_WIDTH)
        self.maze2 = self.generate_maze(PLAY_HEIGHT, PLAY_WIDTH)
        # Draw mazes initially
        self.draw_maze(offset_canvas, self.maze1)
        self.draw_maze(offset_canvas, self.maze2)

    def generate_maze(self, height, width):
        maze = [['#'] * width for _ in range(height)]  # 使用'#'填充迷宫

        # 在迷宫中随机生成起始点和结束点
        start_row, start_col = random.randint(0, height - 1), random.randint(0, width - 1)
        end_row, end_col = random.randint(0, height - 1), random.randint(0, width - 1)

        # 设置起始点和结束点
        maze[start_row][start_col] = 'S'
        maze[end_row][end_col] = 'E'

        # 递归生成迷宫
        self.generate_maze_recursive(maze, start_row, start_col)

        return maze

    def generate_maze_recursive(self, maze, row, col):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # 上下左右四个方向
        random.shuffle(directions)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == '#':
                maze[new_row][new_col] = ' '  # 设置为通道
                maze[row + dr // 2][col + dc // 2] = ' '  # 中间位置也设置为通道
                self.generate_maze_recursive(maze, new_row, new_col)
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

        # 移动玩家1
        self.player1.move(self.maze1, offset_canvas)
        if self.player1.position[0] < 0 or self.player1.position[0] >= PLAY_WIDTH \
                or self.player1.position[1] < 0 or self.player1.position[1] >= PLAY_HEIGHT:
            # 玩家1移动超出边界，将其移回边界内
            self.player1.position = (min(max(self.player1.position[0], 0), PLAY_WIDTH - 1),
                                     min(max(self.player1.position[1], 0), PLAY_HEIGHT - 1))

        # 移动玩家2
        self.player2.move(self.maze2, offset_canvas)
        if self.player2.position[0] < 0 or self.player2.position[0] >= PLAY_WIDTH \
                or self.player2.position[1] < 0 or self.player2.position[1] >= PLAY_HEIGHT:
            # 玩家2移动超出边界，将其移回边界内
            self.player2.position = (min(max(self.player2.position[0], 0), PLAY_WIDTH - 1),
                                     min(max(self.player2.position[1], 0), PLAY_HEIGHT - 1))

        return True
    def draw_maze(self, canvas, maze):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == '#':
                    canvas.SetPixel(col, row, *BLACK)  # 绘制墙壁
                elif maze[row][col] == 'S':
                    canvas.SetPixel(col, row, *YELLOW)  # 绘制起始点
                elif maze[row][col] == 'E':
                    canvas.SetPixel(col, row, *BLUE)  # 绘制结束点
                else:
                    canvas.SetPixel(col, row, *WHITE)  # 绘制通道
    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                

            # Move players and check game status
            running = self.move_players()

            # Draw players
            self.player1.paint(offset_canvas)
            self.player2.paint(offset_canvas)

            # 更新屏幕显示
            matrix.SwapOnVSync(offset_canvas)

            # 设置游戏帧率
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.main()