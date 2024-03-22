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

        # 检查新位置是否为墙，如果是墙则停止移动
        if maze[new_y][new_x] != '#':
            # 更新当前位置
            self.position = (new_x, new_y)

    # 绘制玩家
    def paint(self, canvas):
        canvas.SetPixel(self.position[0], self.position[1], *self.color)

class MazeGame:
    def __init__(self):
        self.maze1, self.start1, self.end1 = self.generate_maze(PLAY_HEIGHT // 2, PLAY_WIDTH)
        self.maze2, self.start2, self.end2 = self.generate_maze(PLAY_HEIGHT // 2, PLAY_WIDTH)

        # 创建玩家对象并赋值给self.player1和self.player2
        self.player1 = Player(YELLOW, GREEN, self.start1)
        self.player2 = Player(BLUE, WHITE, self.start2)
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
    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 移动玩家并检查游戏状态
            running = self.move_players()

            # 绘制迷宫和玩家
            self.draw_maze(offset_canvas, self.maze1)
            self.draw_maze(offset_canvas, self.maze2)
            self.player1.paint(offset_canvas)
            self.player2.paint(offset_canvas)

            # 更新屏幕显示
            matrix.SwapOnVSync()

            # 设置游戏帧率
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.main()