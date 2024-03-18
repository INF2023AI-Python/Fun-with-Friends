import pygame
from rgbmatrix import graphics

# Constants for screen dimensions and options
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32


def draw_level(matrix, offset_canvas):
    # Clear the canvas
    offset_canvas.Clear()

    # Draw the level selection options
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

    # Calculate the center of the screen
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Calculate the positions for centering the text options
    x_position_easy = center_x - 2
    y_position_easy = center_y - 1

    # Add vertical spacing if necessary for additional options
    y_spacing = 4

    # Calculate the position for the "Hard" option
    x_position_hard = center_x - 2
    y_position_hard = y_spacing + y_position_easy + 4  # 4 is the height of one option, so adjust accordingly
    
    turquoise = (0,0,255)
    select_color = graphics.Color(*turquoise)

    # Draw "Easy" option
    graphics.DrawText(offset_canvas, font, x_position_easy, y_position_easy, select_color, "Easy")
    # Draw "Hard" option
    graphics.DrawText(offset_canvas, font, x_position_hard, y_position_hard, select_color, "Hard")

    # Update the display
    matrix.SwapOnVSync(offset_canvas)

def select_level(matrix, offset_canvas, joysticks):
    # Draw the level selection screen
    draw_level(matrix, offset_canvas)

    # Wait for the player to make a selection
    selected_level = None
    while selected_level is None:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Check joystick position to determine the selection
                # Adjust x and y thresholds according to your setup
                if 0.2 < joysticks.get_axis(0) < 0.8 and 0.2 < joysticks.get_axis(1) < 0.8:
                    selected_level = "easy"
                elif -0.8 < joysticks.get_axis(0) < -0.2 and 0.2 < joysticks.get_axis(1) < 0.8:
                    selected_level = "hard"
                # Redraw the screen to highlight the selected option
                draw_level(matrix, offset_canvas)

    return selected_level
