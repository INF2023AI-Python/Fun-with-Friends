# Funktion zum Aktualisieren des Tictactoe-Boards basierend auf Joystick-Eingaben
def update_board_with_joystick(board_state, joystick):
    global current_player
    global orange_square_position

    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Speichern der vorherigen Position für den Vergleich
    previous_position = orange_square_position.copy()

    # Bewegungsrichtung basierend auf den Achsenwerten mit Toleranz
    if -0.2 < x_axis < 0.2 and -0.2 < y_axis < 0.2:
        # Keine Bewegung, wenn keine der Bedingungen erfüllt ist
        return

    # Verfolge die Bewegungsrichtung separat
    if y_axis < -0.8:
        # Bewege nach oben
        orange_square_position[1] = max(0, orange_square_position[1] - 1)
        print("Bewege nach oben")
    elif y_axis > 0.8:
        # Bewege nach unten
        orange_square_position[1] = min(2, orange_square_position[1] + 1)
        print("Bewege nach unten")
    elif x_axis > 0.8:
        # Bewege nach rechts
        orange_square_position[0] = min(2, orange_square_position[0] + 1)
        print("Bewege nach rechts")
    elif x_axis < -0.8:
        # Bewege nach links
        orange_square_position[0] = max(0, orange_square_position[0] - 1)
        print("Bewege nach links")

    # Überprüfe, ob sich die Position geändert hat
    if orange_square_position != previous_position:
        # Aktualisieren des Tic-Tac-Toe-Boards, wenn die Position geändert wurde
        draw_board(board_state)
