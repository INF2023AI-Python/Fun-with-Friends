import time
import pygame
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
import sys


options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0

matrix = RGBMatrix(options=options)


