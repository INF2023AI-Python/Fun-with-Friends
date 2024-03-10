import numpy as np
import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Größe des Spielfelds
ROWS = 8 # 7 leere Zeile, Abstand zwischen Eingabe und Spielfeld!
COLS = 7
CHIP_SIZE = 3

# Erstellen einer leeren Spielfeldmatrix
board = np.zeros((ROWS, COLS), dtype=int)

# RGB-Matrix-Konfiguration
options = RGBMatrixOptions()
options.cols = COLS * CHIP_SIZE
options.rows = ROWS * CHIP_SIZE
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)

def clear_screen():
    matrix.Clear()

# Anzeigen des Spielfelds auf der LED-Matrix
def display_board():
    for row in range(ROWS):
        for col in range(COLS):
            #if not displayed_columns[col]:  # Überprüfen, ob die Spalte bereits angezeigt wurde
                color = (0, 0, 0)  # Standardfarbe für leere Zellen
                if board[row][col] == 1:
                    color = (255, 0, 0)  # Spieler 1: Rot
                elif board[row][col] == 2:
                    color = (0, 0, 255)  # Spieler 2: Blau
                for i in range(CHIP_SIZE):
                    for j in range(CHIP_SIZE):
                        matrix.SetPixel(col * CHIP_SIZE + j + 4, row * CHIP_SIZE + i, *color)

def main():

    pygame.init()
    pygame.joystick.init()

    # Überprüfe, ob ein COntroller angeschlossen ist
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick aus
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


    player = 1
    col = 1
    board[7][1] = 1
    while True:
        clear_screen()
        display_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Dartellung des Chips erstmalig fehlt?

            # Überprüfe die Joystick-Eingaben
            elif event.type == pygame.JOYBUTTONDOWN:
                # Wenn die rot Taste gedrückt wird, dann verscheiben nach rechts
                if event.button == 1:
                    if col < 6:
                        board[7][col] = 0
                        col += 1
                        board[7][col] = player
                    elif col == 6:
                        board[7][col] = 0
                        col = 0
                        board[7][col] = player
                # Wenn die güne Taste gedrückt wird, dann verschieben nach links
                elif event.button == 3:
                    if col > 0:
                        board[7][col] = 0
                        col -= 1
                        board[7][col] = player
                    elif col == 0:
                        board[7][col] = 0
                        col = 6
                        board[7][col] = player
                # Wenn die gelbe Taste gedrückt wird, dann ist es die Eingabe
                #elif event.button == 2:
                    #column = col
                    # Hier muss später der Spielerwechsel stehen

        # Wechseln zum nächsten Spieler
        player = 2 if player == 1 else 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
