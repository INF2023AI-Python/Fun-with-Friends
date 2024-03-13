import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import sys

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0

matrix = RGBMatrix(options=options)

# Startposition des orangenen Quadrats
orange_square_position = [1, 1]

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board(board_state):
    matrix.Clear()
    for row in range(32):
        for col in range(32):
            # Zeichne das Raster
            if row % 10 == 0 or col % 10 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

    # Zeichne die Spielsymbole
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == 'O':
                graphics.DrawCircle(matrix, col * 10 + 5, row * 10 + 5, 4, graphics.Color(0, 0, 255))
            elif board_state[row][col] == 'X':
                x1, y1, x2, y2 = col * 10 + 1, row * 10 + 1, col * 10 + 9, row * 10 + 9
                graphics.DrawLine(matrix, x1, y1, x2, y2, graphics.Color(255, 0, 0))
                graphics.DrawLine(matrix, x2, y1, x1, y2, graphics.Color(255, 0, 0))

    # Zeichne das orangene Quadrat
    x1, y1, x2, y2 = orange_square_position[0] * 10, orange_square_position[1] * 10, (orange_square_position[0] + 1) * 10, (orange_square_position[1] + 1) * 10
    graphics.DrawLine(matrix, x1, y1, x2, y1, graphics.Color(255, 165, 0))
    graphics.DrawLine(matrix, x2, y1, x2, y2, graphics.Color(255, 165, 0))
    graphics.DrawLine(matrix, x2, y2, x1, y2, graphics.Color(255, 165, 0))
    graphics.DrawLine(matrix, x1, y2, x1, y1, graphics.Color(255, 165, 0))

# Funktion zum Überprüfen des Spielstatus (Gewonnen, Unentschieden usw.)
def check_winner(board_state):
    for row in range(3):
        if board_state[row][0] == board_state[row][1] == board_state[row][2] != ' ':
            return True

    for col in range(3):
        if board_state[0][col] == board_state[1][col] == board_state[2][col] != ' ':
            return True

    if board_state[0][0] == board_state[1][1] == board_state[2][2] != ' ':
        return True

    if board_state[0][2] == board_state[1][1] == board_state[2][0] != ' ':
        return True

    return False

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
        # Wenn die Position geändert wurde, zeichnen Sie das Tic-Tac-Toe-Board neu
        draw_board(board_state)

# Funktion für die Hauptschleife des Spiels
def tictactoe():
    global current_player
    global orange_square_position

    # Tictactoe-Board initialisieren
    board_state = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'  # Initialisieren Sie die Variable global

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Please connect a joystick and try again.")
        pygame.quit()
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(board_state)
        update_board_with_joystick(board_state, joystick)

        # Überprüfen Sie den Gewinner und den Unentschieden-Status
        if check_winner(board_state):
            draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
            print(f"Player {current_player} wins!")
            return
        elif ' ' not in [cell for row in board_state for cell in row]:
            draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
            print("It's a draw!")
            return

        pygame.time.Clock().tick(10)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen

# Hauptausführung des Programms
if __name__ == "__main__":
    tictactoe()
