import pygame
from rgbmatrix import graphics
from obstacle import obstacle, maze


# Constants for screen dimensions and options
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

def draw_level(matrix, offset_canvas, selected_level):
    # Clear the canvas
    offset_canvas.Clear()

    # Set the font for the selection page
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

    # Calculate the center of the screen
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Calculate the positions for the "Easy" option
    x_position_easy = center_x - 10
    y_position_easy = center_y - 1

    # Add vertical spacing
    y_spacing = 4

    # Calculate the position for the "Hard" option
    x_position_hard = center_x - 10
    y_position_hard = y_spacing + y_position_easy + 4
    
    # Set the default color
    default_color = graphics.Color(255, 255, 255)

    # Set the selected color to red
    selected_color = graphics.Color(255, 0, 0)

    # Draw "Easy" option
    if selected_level == "easy":
        graphics.DrawText(offset_canvas, font, x_position_easy, y_position_easy, selected_color, "Easy")
    else:
        graphics.DrawText(offset_canvas, font, x_position_easy, y_position_easy, default_color, "Easy")
    
    # Draw "Hard" option
    if selected_level == "hard":
        graphics.DrawText(offset_canvas, font, x_position_hard, y_position_hard, selected_color, "Hard")
    else:
        graphics.DrawText(offset_canvas, font, x_position_hard, y_position_hard, default_color, "Hard")

    # Update the display
    matrix.SwapOnVSync(offset_canvas)
    
def select_level(matrix, offset_canvas, joysticks):
    # initialise the level to be easy
    selected_level = "easy"
    # draw the selection page
    draw_level(matrix, offset_canvas, selected_level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    selected_level = "easy"
                    draw_level(matrix, offset_canvas, selected_level)
                if event.button == 2:
                    selected_level = "hard"
                    draw_level(matrix, offset_canvas, selected_level)
                if event.button == 1:
                    # submit the choice
                    if selected_level == "hard":
                        return "hard"
                        # return maze(offset_canvas, matrix)
                    if selected_level == "easy":
                        return "easy"
                        # return obstacle(offset_canvas, matrix)

        pygame.time.Clock().tick(10)