import pygame
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from time import time
from players_init import players_init

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.columns = 32

matrix = RGBMatrix(options)
canvas = matrix.CreateFrameCanvas()


game_duration = 60

pygame.joystick.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


def game_init():

    pygame.init()
    player_data = players_init()
    player1 = player_data.copy()
    player2 = player_data.copy()

    return player1, player2


def game_controllers(controllers, player1, player2):
    for controller in controllers:
        # Handle joystick axis motion
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # Check if the controller is Player 1's
                if controller == player1.controller:
                    # Handle Player 1's joystick axis motion
                    player1.handle_axis_motion(event.axis, event.value)
                # Check if the controller is Player 2's
                elif controller == player2.controller:
                    # Handle Player 2's joystick axis motion
                    player2.handle_axis_motion(event.axis, event.value)
            # Handle joystick button press or release
            elif event.type == pygame.JOYBUTTONDOWN:
                # Check if the controller is Player 1's
                if controller == player1.controller:
                    # Handle Player 1's button press
                    player1.handle_button_press(event.button)
                # Check if the controller is Player 2's
                elif controller == player2.controller:
                    # Handle Player 2's button press
                    player2.handle_button_press(event.button)

