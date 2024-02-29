import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

# Pygame initialisieren
pygame.init()
pygame.joystick.init()

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board(board_state):
    matrix.Clear()
    for row in range(32):
        for col in range(32):
            # Zeichne das Raster
            if row % 11 == 0 or col % 11 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

    # Zeichne die Spielsymbole
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == 'O':
                graphics.DrawCircle(matrix, col * 11 + 5, row * 11 + 5, 4, graphics.Color(0, 0, 255))
            elif board_state[row][col] == 'X':
                graphics.DrawLine(matrix, col * 11 + 1, row * 11 + 1, col * 11 + 9, row * 11 + 9, graphics.Color(255, 0, 0))
                graphics.DrawLine(matrix, col * 11 + 9, row * 11 + 1, col * 11 + 1, row * 11 + 9, graphics.Color(255, 0, 0))

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

# Funktion zum Zeichnen der Linie für den Gewinner
def draw_winner_line(start_row, start_col, end_row, end_col):
    graphics.DrawLine(matrix, start_col, start_row, end_col, end_row, graphics.Color(0, 255, 0))

# Funktion zum Konvertieren von Pygame-Eingaben zu Spielfeldpositionen
def pygame_to_position(event):
    if event.type == pygame.JOYBUTTONDOWN:
        # Buttons auf dem Gamepad
        button_mapping = {
            0: (0, 0),  # Beispiel: Button 0 setzt das Symbol in die obere linke Ecke
            1: (0, 1),
            2: (0, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (2, 0),
            7: (2, 1),
            8: (2, 2),
        }
        if event.button in button_mapping:
            return button_mapping[event.button]

    return None

# Hauptspiel-Schleife
while True:
    # Tictactoe-Board initialisieren
    board_state = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'

    while True:
        draw_board(board_state)

        for event in pygame.event.get():
            position = pygame_to_position(event)
            if position is not None:
                row, col = position

                # Überprüfen, ob das Feld bereits belegt ist
                if 0 <= row <= 2 and 0 <= col <= 2 and board_state[row][col] == ' ':
                    # Zug durchführen
                    board_state[row][col] = current_player

                    # Spielstatus überprüfen
                    if check_winner(board_state):
                        draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
                        print(f"Player {current_player} wins!")
                        break
                    elif ' ' not in [cell for row in board_state for cell in row]:
                        draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
                        print("It's a draw!")
                        break

                    # Spieler wechseln
                    current_player = 'X' if current_player == 'O' else 'O'
                else:
                    print("Invalid move. Try again.")

        time.sleep(0.1)  # Fügt eine kurze Verzögerung hinzu, um die Abfragefrequenz zu steuern

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        break

# Pygame beenden
pygame.joystick.quit()
pygame.quit()
