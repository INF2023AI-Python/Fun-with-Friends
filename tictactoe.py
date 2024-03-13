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
def draw_board(board_state, current_player):
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

    # Anzeige des aktuellen Spielers
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
    if current_player == 'X':
        graphics.DrawText(matrix, font, 0, 0, graphics.Color(255, 0, 0), "Current Player: X")
    else:
        graphics.DrawText(matrix, font, 0, 0, graphics.Color(0, 0, 255), "Current Player: O")

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
def update_board_with_joystick(board_state, joystick, current_player):
    global orange_square_position

    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Bewegungsrichtung basierend auf den Achsenwerten mit Toleranz
    if -0.2 < x_axis < 0.2 and y_axis < -0.8:
        # Bewege nach oben
        orange_square_position[1] = max(0, orange_square_position[1] - 1)
    elif -0.2 < x_axis < 0.2 and y_axis > 0.8:
        # Bewege nach unten
        orange_square_position[1] = min(2, orange_square_position[1] + 1)
    elif x_axis > 0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach rechts
        orange_square_position[0] = min(2, orange_square_position[0] + 1)
    elif x_axis < -0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach links
        orange_square_position[0] = max(0, orange_square_position[0] - 1)

    # Überprüfe, ob der Button mit der ID 0 gedrückt wurde
    if joystick.get_button(0) == 1:
        set_x_or_o(board_state, current_player)

# Funktion zum Setzen von 'X' oder 'O' auf dem Tictactoe-Board
def set_x_or_o(board_state, current_player):
    global orange_square_position

    # Überprüfe, ob das ausgewählte Feld leer ist (' ')
    if board_state[orange_square_position[1]][orange_square_position[0]] == ' ':
        board_state[orange_square_position[1]][orange_square_position[0]] = current_player

# Funktion für die Hauptschleife des Spiels
def tictactoe():
    # Tictactoe-Board initialisieren
    board_state = [[' ' for _ in range(3)] for _ in range(3)]

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("Kein Joystick erkannt. Bitte schließen Sie einen Joystick an und versuchen Sie es erneut.")
        pygame.quit()
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    current_player = 'X'  # Starten Sie mit Spieler 1 (X)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(board_state, current_player)
        update_board_with_joystick(board_state, joystick, current_player)

        # Überprüfen Sie den Gewinner und den Unentschieden-Status
        if check_winner(board_state):
            print(f"Player {current_player} wins!")
            return
        elif ' ' not in [cell for row in board_state for cell in row]:
            print("Unentschieden!")
            return

        pygame.time.Clock().tick(10)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen

# Hauptausführung des Programms
if __name__ == "__main__":
    tictactoe()
