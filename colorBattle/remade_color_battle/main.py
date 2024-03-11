from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
# from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pygame
from time import time
import random
# from colorBattle.remade_color_battle.movement import wrapping, input
import obstacle

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
GAME_DURATION = 60

width, height = 32, 32
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()


# global player1_x, player1_y, player2_x, player2_y, game_area, player_size
# player1_speed = 10
# player2_speed = 10
# game_area = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

# initialise
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


def main():
    running = True
    while running:
        if event.type == pygame.QUIT:
                running = False

        clock = pygame.time.Clock()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #read input, keep players in the area
        # wrapping()
        # input(joysticks)

        #draw obstacle
        obstacle()



        clock.tick(60)
    pygame.quit()


