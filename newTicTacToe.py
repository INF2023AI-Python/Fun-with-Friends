import pygame
import sys
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
width, height = 300, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            row = mouseY // (height // 3)
            col = mouseX // (width // 3)

            # Überprüfen, ob das Feld bereits belegt ist
            if board_state[row][col] == ' ':
                # Zug durchführen
                board_state[row][col] = current_player

                # Spielstatus überprüfen
                if check_winner():
                    draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
                    print(f"Player {current_player} wins!")
                    pygame.quit()
                    sys.exit()
                elif ' ' not in [cell for row in board_state for cell in row]:
                    draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
                    print("It's a draw!")
                    pygame.quit()
                    sys.exit()

                # Spieler wechseln
                current_player = 'O' if current_player == 'X' else 'X'

    draw_board()
    pygame.display.flip()
