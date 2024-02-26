import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

# Tictactoe-Board initialisieren
board_state = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'O'

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    matrix.Clear()
    for row in range(31):
        for col in range(31):
            # Zeichne das Raster
            if row % 10 == 0 or col % 10 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

    # Zeichne die Spielsymbole
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == 'O':
                graphics.DrawText(matrix, graphics.Font(), col * 10 + 2, row * 10 + 2, graphics.Color(0, 0, 255), "O")
            elif board_state[row][col] == 'X':
                graphics.DrawText(matrix, graphics.Font(), col * 10 + 2, row * 10 + 2, graphics.Color(255, 0, 0), "X")

# Funktion zum Überprüfen des Spielstatus (Gewonnen, Unentschieden usw.)
def check_winner():
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
    draw_board()

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
        if check_winner():
