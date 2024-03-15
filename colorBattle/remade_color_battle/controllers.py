def controllers(joysticks, player1, player2):
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            if axis_x < 0:
                player1.move('LEFT')
            elif axis_x > 0:
                player1.move('RIGHT')
            if axis_y < 0:
                player1.move('UP')
            elif axis_y > 0:
                player1.move('DOWN')

        elif i == 1:  # Player 2 controls (Second gamepad)
            if axis_x < 0:
                player2.move('LEFT')
            elif axis_x > 0:
                player2.move('RIGHT')
            if axis_y < 0:
                player2.move('UP')
            elif axis_y > 0:
                player2.move('DOWN')
