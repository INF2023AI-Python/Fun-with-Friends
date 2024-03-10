import RGBMatrixEmulator
import pygame

#global variable in main
global player1_speed, player2_speed, player_size
#constant in main
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
GAME_DURATION = 60


joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

def input(joysticks):
#in main game loop
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * player1_speed)
            player1_y += int(axis_y * player1_speed)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)


def wrapping():
    # Wrap player 1 around the screen borders
    if player1_x < 0:
        player1_x = PLAY_WIDTH - player_size
    elif player1_x >= PLAY_WIDTH:
        player1_x = 0
    if player1_y < 0:
        player1_y = PLAY_HEIGHT - player_size
    elif player1_y >= PLAY_HEIGHT:
        player1_y = 0

    # Wrap player 2 around the screen borders
    if player2_x < 0:
        player2_x = PLAY_WIDTH - player_size
    elif player2_x >= PLAY_WIDTH:
        player2_x = 0
    if player2_y < 0:
        player2_y = PLAY_HEIGHT - player_size
    elif player2_y >= PLAY_HEIGHT:
        player2_y = 0

    player1_x = max(0, min(PLAY_WIDTH - player_size, player1_x))
    player1_y = max(0, min(PLAY_HEIGHT - player_size, player1_y))

    player2_x = max(0, min(PLAY_WIDTH - player_size, player2_x))
    player2_y = max(0, min(PLAY_HEIGHT - player_size, player2_y))
