def controllers(joysticks, player1, player2, maze_pattern, game_area):
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            if -0.2 < axis_x < 0.2 and axis_y < -0.8:
                player1.move('UP', maze_pattern, game_area)
            elif -0.2 < axis_x < 0.2 and axis_y > 0.8:
                player1.move('DOWN', maze_pattern, game_area)
            elif axis_x > 0.8 and -0.2 < axis_y < 0.2:
                player1.move('RIGHT', maze_pattern, game_area)
            elif axis_x < -0.8 and -0.2 < axis_y < 0.2:
                player1.move('LEFT', maze_pattern, game_area)

        elif i == 1:  # Player 2 controls (Second gamepad)
            if -0.2 < axis_x < 0.2 and axis_y < -0.8:
                player2.move('UP', maze_pattern, game_area)
            elif -0.2 < axis_x < 0.2 and axis_y > 0.8:
                player2.move('DOWN', maze_pattern, game_area)
            elif axis_x > 0.8 and -0.2 < axis_y < 0.2:
                player2.move('RIGHT', maze_pattern, game_area)
            elif axis_x < -0.8 and -0.2 < axis_y < 0.2:
                player2.move('LEFT', maze_pattern, game_area)
