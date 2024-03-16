import pygame
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from colorBattle.remade_color_battle.new import update_canvas
from players_init import players_init

# Global variables
global player1_speed, player2_speed, player_size

# Constants
ROWS = 32
COLS = 28


def controllers(joysticks, player1_x, player1_y, player2_x, player2_y):
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * player1_speed)
            player1_y += int(axis_y * player1_speed)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)

        if player1_x < 0:
            player1_x = ROWS - player_size
        elif player1_x >= ROWS:
            player1_x = 0
        if player1_y < 0:
            player1_y = COLS - player_size
        elif player1_y >= COLS:
            player1_y = 0

        if player2_x < 0:
            player2_x = ROWS - player_size
        elif player2_x >= ROWS:
            player2_x = 0
        if player2_y < 0:
            player2_y = COLS - player_size
        elif player2_y >= COLS:
            player2_y = 0

        player1_x = max(0, min(ROWS - player_size, player1_x))
        player1_y = max(0, min(COLS - player_size, player1_y))

        player2_x = max(0, min(ROWS - player_size, player2_x))
        player2_y = max(0, min(COLS - player_size, player2_y))

    return player1_x, player1_y, player2_x, player2_y


# def update_canvas(canvas, player1_x, player1_y, player2_x, player2_y):
#     # Clear the canvas
#     canvas.Clear()
#
#     # Draw players
#     canvas.SetPixel(player1_x, player1_y, 255, 0, 0)  # Red color for Player 1
#     canvas.SetPixel(player2_x, player2_y, 0, 0, 255)  # Blue color for Player 2
#
#     # Update the display
#     canvas = matrix.SwapOnVSync()  # Use SwapOnVSync to update the display


# Main function
def main():
    pygame.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Initialize the RGBMatrixEmulator
    options = RGBMatrixOptions()
    options.hardware_mapping = 'adafruit-hat'
    options.rows = COLS
    options.cols = ROWS
    matrix = RGBMatrix(options)
    canvas = matrix.CreateFrameCanvas()

    player_positions = players_init()
    player1_x, player1_y, player2_x, player2_y = player_positions['player1_x'], player_positions['player1_y'], player_positions['player2_x'], player_positions['player2_y']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        player1_x, player1_y, player2_x, player2_y = controllers(joysticks, player1_x, player1_y, player2_x, player2_y)

        update_canvas(canvas, player1_x, player1_y, player2_x, player2_y)

        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main()
