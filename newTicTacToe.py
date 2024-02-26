import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

# Tictactoe-Board initialisieren
board_state = [[' ' for _ in range(32)] for _ in range(32)]
current_player = 'X'

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    matrix.Clear()
    for row in range(32):
        for col in range(32):
            # Zeichne das Raster
            if row % 10 == 0 or col % 10 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

            # Zeichne die Spielsymbole
            if board_state[row][col] == 'X':
                matrix.SetPixel(col, row, 255, 0, 0)
            elif board_state[row][col] == 'O':
                matrix.SetPixel(col, row, 0, 0, 255)

# Funktion zum Überprüfen des Spielstatus (Gewonnen, Unentschieden usw.)
def check_winner():
    for row in range(32):
        for col in range(32):
            if board_state[row][col] == ' ':
                continue

            # Überprüfen Sie horizontal
            if col + 4 <= 32 and len(set(board_state[row][col:col + 4])) == 1:
                return True

            # Überprüfen Sie vertikal
            if row + 4 <= 32 and len(set(board_state[row + i][col] for i in range(4))) == 1:
                return True

            # Überprüfen Sie diagonal von links oben nach rechts unten
            if row + 4 <= 32 and col + 4 <= 32 and len(set(board_state[row + i][col + i] for i in range(4))) == 1:
                return True

            # Überprüfen Sie diagonal von links unten nach rechts oben
            if row - 4 >= 0 and col + 4 <= 32 and len(set(board_state[row - i][col + i] for i in range(4))) == 1:
                return True

    return False

# Hauptspiel-Schleife
while True:
    draw_board()

    try:
        row = int(input("Enter row (0 to 31): "))
        col = int(input("Enter column (0 to 31): "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    # Überprüfen, ob das Feld bereits belegt ist
    if 0 <= row <= 31 and 0 <= col <= 31 and board_state[row][col] == ' ':
        # Zug durchführen
        board_state[row][col] = current_player

        # Spielstatus überprüfen
        if check_winner():
            draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um den Gewinner anzuzeigen
            print(f"Player {current_player} wins!")
            break
        elif ' ' not in [cell for row in board_state for cell in row]:
            draw_board()  # Aktualisiere das letzte Mal vor dem Ende, um das Unentschieden anzuzeigen
            print("It's a draw!")
            break

        # Spieler wechseln
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("Invalid move. Try again.")
    
    time.sleep(0.5)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen
