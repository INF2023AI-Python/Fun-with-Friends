def controllers(joysticks, player1, player2, maze_pattern, game_area):
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            if axis_x < -0.5:
                player1.move('LEFT', maze_pattern, game_area)
            elif axis_x > 0.5:
                player1.move('RIGHT', maze_pattern, game_area)
            if axis_y < -0.5:
                player1.move('UP', maze_pattern, game_area)
            elif axis_y > 0.5:
                player1.move('DOWN', maze_pattern, game_area)

        elif i == 1:  # Player 2 controls (Second gamepad)
            if axis_x < -0.5:
                player2.move('LEFT', maze_pattern, game_area)
            elif axis_x > 0.5:
                player2.move('RIGHT', maze_pattern, game_area)
            if axis_y < -0.5:
                player2.move('UP', maze_pattern, game_area)
            elif axis_y > 0.5:
                player2.move('DOWN', maze_pattern, game_area)

