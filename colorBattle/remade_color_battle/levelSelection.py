def select_level(matrix, offset_canvas, joysticks):
    # Initialize the selected level as None
    selected_level = None

    # Initialize the previous joystick position
    prev_x_axis = 0
    prev_y_axis = 0

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
            
            # Redraw the screen to highlight the selected option only if the joystick position has changed
            if x_axis != prev_x_axis or y_axis != prev_y_axis:
                draw_level(matrix, offset_canvas, selected_level)

            # Update previous joystick position
            prev_x_axis = x_axis
            prev_y_axis = y_axis
        
        pygame.time.Clock().tick(10)

    return selected_level