import pygame
from rgbmatrix import graphics

# Constants for screen dimensions and options
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

def draw_level(matrix, offset_canvas, selected_level):
    # Clear the canvas
    offset_canvas.Clear()

    # Draw the level selection options
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

    # Calculate the center of the screen
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Calculate the positions for centering the text options
    x_position_easy = center_x - 10
    y_position_easy = center_y - 1

    # Set the default color
    default_color = graphics.Color(255, 255, 255)

    # Set the selected color to red
    selected_color = graphics.Color(255, 0, 0)

    # Draw "Easy" option
    if selected_level == "easy":
        graphics.DrawText(offset_canvas, font, x_position_easy, y_position_easy, selected_color, "Easy")
    else:
        graphics.DrawText(offset_canvas, font, x_position_easy, y_position_easy, default_color, "Easy")

    # Update the display
    matrix.SwapOnVSync(offset_canvas)

def select_level(matrix, offset_canvas, joysticks):
    # Draw the level selection screen
    selected_level = None
    while selected_level is None:
        draw_level(matrix, offset_canvas, selected_level)
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Check joystick position to determine the selection
                if 0.2 < joysticks.get_axis(0) < 0.8 and 0.2 < joysticks.get_axis(1) < 0.8:
                    selected_level = "easy"
                elif -0.8 < joysticks.get_axis(0) < -0.2 and 0.2 < joysticks.get_axis(1) < 0.8:
                    selected_level = "hard"

    return selected_level