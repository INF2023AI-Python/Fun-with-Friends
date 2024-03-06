import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import sys

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

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
                graphics.DrawLine(matrix, col * 10 + 1, row * 10 + 1, col * 10 + 9, row * 10 + 9, graphics.Color(255, 0, 0))
                graphics.DrawLine(matrix, col * 10 + 9, row * 10 + 1, col * 10 + 1, row * 10 + 9, graphics.Color(255, 0, 0))

# Funktion zum Überprüfen des Spielstatus (Gewonnen, Unentschieden usw.)
def check_winner(board_state):
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == ' ':
                continue

            # Überprüfen Sie horizontal
            if col + 2 < 3 and len(set(board_state[row][col:col + 3])) == 1:
                return True

            # Überprüfen Sie vertikal
            if row + 2 < 3 and len(set(board_state[row + i][col] for i in range(3))) == 1:
                return True

            # Überprüfen Sie diagonal von links oben nach rechts unten
            if row + 2 < 3 and col + 2 < 3 and len(set(board_state[row + i][col + i] for i in range(3))) == 1:
                return True

            # Überprüfen Sie diagonal von links unten nach rechts oben
            if row - 2 >= 0 and col + 2 < 3 and len(set(board_state[row - i][col + i] for i in range(3))) == 1:
                return True

    return False

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Initialisiere die Position des Quadrats
square_x, square_y = 0, 0

# Tictactoe-Board initialisieren
board_state = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'O'

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Button 0 drücken (nach oben bewegen)
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            square_y = max(square_y - 10, 0)

        # Button 1 drücken (nach rechts bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 1:
            square_x = min(square_x + 10, 20)

        # Button 2 drücken (nach unten bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
            square_y = min(square_y + 10, 20)

        # Button 3 drücken (nach links bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 3:
            square_x = max(square_x - 10, 0)

        # Button 5 drücken (Bestätigung)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 5:
            row, col = square_y // 10, square_x // 10

            # Überprüfen, ob das Feld bereits belegt ist
            if 0 <= row <= 2 and 0 <= col <= 2 and board_state[row][col] == ' ':
                # Zug durchführen
                board_state[row][col] = 'X' if current_player == 'X' else 'O'

                # Spielstatus überprüfen
                if check_winner(board_state):
                    draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
                    print(f"Player {current_player} wins!")
                    time.sleep(1)
                elif ' ' not in [cell for row in board_state for cell in row]:
                    draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
                    print("It's a draw!")
                    time.sleep(1)

                # Spieler wechseln
                current_player = 'X' if current_player == 'O' else 'O'

    # Tictactoe-Board und Quadrat zeichnen
    draw_board(board_state)
    graphics.DrawLine(matrix, square_x, square_y, square_x + 10, square_y, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, square_x, square_y, square_x, square_y + 10, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, square_x + 10, square_y, square_x + 10, square_y + 10, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, square_x, square_y + 10, square_x + 10, square_y + 10, graphics.Color(255, 0, 0))

    time.sleep(1)  # Fügt eine kurze Verzögerung hinzu, um die Bewegung sichtbar zu machen
