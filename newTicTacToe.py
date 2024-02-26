import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

# Tictactoe-Board initialisieren
board_state = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    matrix.Clear()
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == 'X':
                matrix.SetPixel(col * 10, row * 10, 255, 0, 0)
                matrix.SetPixel(col * 10 + 1, row * 10, 255, 0, 0)
                matrix.SetPixel(col * 10, row * 10 + 1, 255, 0, 0)
                matrix.SetPixel(col * 10 + 1, row * 10 + 1, 255, 0, 0)
            elif board_state[row][col] == 'O':
                matrix.SetPixel(col * 10 + 5, row * 10 + 5, 0, 0, 255)

# Funktion zum Überprüfen des Spielstatus (Gewonnen, Unentschieden usw.)
def check_winner():
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

# Hauptspiel-Schleife
pygame.init()

while True:
    draw_board()

    # Tastatureingaben abfragen
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                row, col = 0, 0
            elif event.key == pygame.K_2:
                row, col = 0, 1
            elif event.key == pygame.K_3:
                row, col = 0, 2
            elif event.key == pygame.K_4:
                row, col = 1, 0
            elif event.key == pygame.K_5:
                row, col = 1, 1
            elif event.key == pygame.K_6:
                row, col = 1, 2
            elif event.key == pygame.K_7:
                row, col = 2, 0
            elif event.key == pygame.K_8:
                row, col = 2, 1
            elif event.key == pygame.K_9:
                row, col = 2, 2
            else:
                continue

            # Überprüfen, ob das Feld bereits belegt ist
            if board_state[row][col] == ' ':
                # Zug durchführen
                board_state[row][col] = current_player

                # Spielstatus überprüfen
                if check_winner():
                    draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
                    print(f"Player {current_player} wins!")
                    pygame.quit()
                    exit()
                elif ' ' not in [cell for row in board_state for cell in row]:
                    draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
                    print("It's a draw!")
                    pygame.quit()
                    exit()

                # Spieler wechseln
                current_player = 'O' if current_player == 'X' else 'X'

    pygame.time.Clock().tick(10)  # Begrenzen Sie die Framerate auf 10 FPS
