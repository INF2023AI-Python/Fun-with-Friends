from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import pygame
from time import time
import random
# from colorBattle.remade_color_battle.movement import wrapping, input


# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
GAME_DURATION = 60


global player1_x, player1_y, player2_x, player2_y, game_area, player_size
player1_speed = 10
player2_speed = 10
game_area = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

# initialise
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


def main():

    while True:
        wrapping()
        input()


