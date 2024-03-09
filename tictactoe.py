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
    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Aktualisiere die Position basierend auf den Achsenwerten
    if x_axis < -0.5:
        move_left(board_state)
    elif x_axis > 0.5:
        move_right(board_state)

    if y_axis < -0.5:
        move_up(board_state)
    elif y_axis > 0.5:
        move_down(board_state)

# Hilfsfunktionen für die Joystick-Bewegungen
def move_left(board_state):
    board_state[0] = ['O', ' ', 'X'] if board_state[0][0] == ' ' else board_state[0]

def move_right(board_state):
    board_state[2] = ['X', ' ', 'O'] if board_state[2][2] == ' ' else board_state[2]

def move_up(board_state):
    board_state = [list(row) for row in zip(*board_state)]
    move_left(board_state)
    board_state = [list(row) for row in zip(*board_state)]

def move_down(board_state):
    board_state = [list(row) for row in zip(*board_state)]
    move_right(board_state)
    board_state = [list(row) for row in zip(*board_state)]

# Hauptspiel-Schleife
while True:
    # Tictactoe-Board initialisieren
    board_state = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'O'

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Please connect a joystick and try again.")
        pygame.quit()
        break

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        draw_board(board_state)
        update_board_with_joystick(board_state, joystick)

        # Überprüfen Sie den Gewinner und den Unentschieden-Status
        if check_winner(board_state):
            draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
            print(f"Player {current_player} wins!")
            break
        elif ' ' not in [cell for row in board_state for cell in row]:
            draw_board(board_state)  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
            print("It's a draw!")
            break

        pygame.time.Clock().tick(10)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen

    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again != 'yes':
        break
