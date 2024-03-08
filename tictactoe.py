import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import sys

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    sys.exit()
else:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"Joystick {i + 1} detected. ID: {joystick.get_id()}")

joystick = pygame.joystick.Joystick(0)
joystick.init()

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

# Hauptspiel-Schleife
while True:
    # Tictactoe-Board initialisieren
    board_state = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'

    while True:
        draw_board(board_state)

        try:
            row = int(input("Enter row (0 to 2): "))
            col = int(input("Enter column (0 to 2): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

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
        
        time.sleep(0.5)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        break
