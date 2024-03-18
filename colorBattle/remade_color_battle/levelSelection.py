import pygame
from rgbmatrix import graphics

# Constants for screen dimensions and options
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

# Coordinates for the square areas representing easy and hard options
EASY_SQUARE = [(5, 10), (15, 10), (5, 18), (15, 18)]
HARD_SQUARE = [(5, 18), (15, 18), (5, 26), (15, 26)]

def draw_level(matrix, offset_canvas, selected_level):
    # Clear the canvas
    offset_canvas.Clear()

    # Draw the level selection options
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

    # Set the default color
    default_color = graphics.Color(255, 255, 255)

    # Set the selected color to red
    selected_color = graphics.Color(255, 0, 0)

    # Draw "Easy" square
    for x, y in EASY_SQUARE:
        graphics.DrawLine(offset_canvas, x, y, x + 8, y, default_color)
        graphics.DrawLine(offset_canvas, x + 8, y, x + 8, y + 8, default_color)
        graphics.DrawLine(offset_canvas, x + 8, y + 8, x, y + 8, default_color)
        graphics.DrawLine(offset_canvas, x, y + 8, x, y, default_color)
    
    # Draw "Hard" square
    for x, y in HARD_SQUARE:
        graphics.DrawLine(offset_canvas, x, y, x + 8, y, default_color)
        graphics.DrawLine(offset_canvas, x + 8, y, x + 8, y + 8, default_color)
        graphics.DrawLine(offset_canvas, x + 8, y + 8, x, y + 8, default_color)
        graphics.DrawLine(offset_canvas, x, y + 8, x, y, default_color)

    # Draw "Easy" and "Hard" texts
    graphics.DrawText(offset_canvas, font, 7, 12, selected_color if selected_level == "easy" else default_color, "Easy")
    graphics.DrawText(offset_canvas, font, 7, 20, selected_color if selected_level == "hard" else default_color, "Hard")

    # Update the display
    matrix.SwapOnVSync(offset_canvas)

def select_level(matrix, offset_canvas, joysticks):
    # Initialize the selected level as None
    selected_level = None

    while selected_level is None:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Check if button 0 (button A) is pressed
                if event.button == 0:
                    # Return the selected level
                    return selected_level
                
        # Check joystick position to determine the selection
        for joystick in joysticks:
            # Get current joystick position
            x_axis = joystick.get_axis(0)
            y_axis = joystick.get_axis(1)

            # Determine the selected level based on joystick position
            if 0.2 < x_axis < 0.8 and 0.2 < y_axis < 0.8:
                selected_level = "easy"
            elif -0.8 < x_axis < -0.2 and 0.2 < y_axis < 0.8:
                selected_level = "hard"
            
        # Redraw the screen to highlight the selected option
        draw_level(matrix, offset_canvas, selected_level)
        
        pygame.time.Clock().tick(10)

    return selected_level
