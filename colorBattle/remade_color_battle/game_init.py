from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
import pygame

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.columns = 32

matrix = RGBMatrix(options)


def game_init():

    pygame.init()
    pygame.joystick.init()



