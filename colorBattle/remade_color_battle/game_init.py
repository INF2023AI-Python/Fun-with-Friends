from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import pygame
from players import players_init


options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.columns = 32

matrix = RGBMatrix(options)
canvas = matrix.CreateFrameCanvas()


def game_init():

    pygame.init()


def game_controllers():

    pygame.joystick.init()

    controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


