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

    # Add vertical spacing if necessary for additional options
    y_spacing = 4

    # Calculate the position for the "Hard" option
    x_position_hard = center_x - 10
    y_position_hard = y_spacing + y_position_easy + 4  # 4 is the height of one option, so adjust accordingly
    
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


