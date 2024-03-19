

def controllers(joysticks, player1, player2, maze_pattern, game_area):
    DEAD_ZONE = 0.07  # Adjust this value to increase or decrease the dead zone
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(1)  # Swap the axes
        axis_y = joystick.get_axis(0)  # Swap the axes

        if abs(axis_x) < DEAD_ZONE:
            axis_x = 0
        if abs(axis_y) < DEAD_ZONE:
            axis_y = 0

        if i == 0:  # Player 1 controls (First gamepad)
            if axis_x < -DEAD_ZONE:
                player1.move('LEFT', maze_pattern, game_area)
            elif axis_x > DEAD_ZONE:
                player1.move('RIGHT', maze_pattern, game_area)
            if axis_y < -DEAD_ZONE:
                player1.move('UP', maze_pattern, game_area)
            elif axis_y > DEAD_ZONE:
                player1.move('DOWN', maze_pattern, game_area)

        elif i == 1:  # Player 2 controls (Second gamepad)
            if axis_x < -DEAD_ZONE:
                player2.move('LEFT', maze_pattern, game_area)
            elif axis_x > DEAD_ZONE:
                player2.move('RIGHT', maze_pattern, game_area)
            if axis_y < -DEAD_ZONE:
                player2.move('UP', maze_pattern, game_area)
            elif axis_y > DEAD_ZONE:
                player2.move('DOWN', maze_pattern, game_area)

        print(f"Joystick {i}: axis_x = {axis_x}, axis_y = {axis_y}")
