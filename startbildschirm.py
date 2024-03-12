import numpy as np
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

SIZE = 1  # Größe 1
SIZE_FIELD = 16

# Leeres Array für die Piktogramme
selection = np.zeros((SIZE, SIZE), dtype=int)

# Konfiguration der Matrix
options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)

# Funktion zum Löschen des Bildschirms
def clear_screen():
    matrix.Clear()

# Funktion zum Zeichnen des Bildschirms
def draw_screen():
    # Farbe der Linie (weiß)
    color = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    # Zeichnen der vertikalen Linie
    for row in range(32):
        matrix.SetPixel(0, row, *color)
        matrix.SetPixel(15, row, *color)
        matrix.SetPixel(31, row, *color)

    # Zeichnen der horizontalen Linie
    for col in range(32):
        matrix.SetPixel(col, 0, *color)
        matrix.SetPixel(col, 15, *color)
        matrix.SetPixel(col, 31, *color)

    # Zeichnen der Piktogramme
    # Colorbattel
    for row in range(2, 7):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *red)
    for row in range(9, 14):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *blue)

    # tictactoe
    positionsX = [
        (17, 4), (18, 5), (19, 6), (20, 7), (21, 6), (22, 5), (23, 4),
        (19, 8), (21, 8), (18, 9), (22, 9), (17, 10), (23, 10)
    ]
    for pos in positionsX:
        matrix.SetPixel(pos[0], pos[1], *red)
    positionsO = [
        (24, 6), (24, 7), (24, 8), (25, 5), (25, 9), (26, 4), (26, 10),
        (27, 4), (27, 10), (28, 5), (28, 9), (29, 6), (29, 7), (29, 8)
    ]
    for pos in positionsO:
        matrix.SetPixel(pos[0], pos[1], *blue)

    # VierGewinnt
    for row in range(2, 5):
        for col in range(27, 30):
            matrix.SetPixel(row, col, *red)
    for row in range(5, 8):
        for col in range(24, 30):
            matrix.SetPixel(row, col, *blue)
    for row in range(8, 11):
        for col in range(21, 30):
            matrix.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(18, 24):
            matrix.SetPixel(row, col, *blue)
    for row in range(11, 14):
        for col in range(24, 27):
            matrix.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(27, 30):
            matrix.SetPixel(row, col, *blue)

    # ShutDown
    for row in range(23, 25):
        for col in range(18, 24):
            matrix.SetPixel(row, col, *red)
    for row in range(22, 26):
        for col in range(28, 30):
            matrix.SetPixel(row, col, *red)
    for row in range(20, 22):
        for col in range(26, 28):
            matrix.SetPixel(row, col, *red)
    for row in range(26, 28):
        for col in range(26, 28):
            matrix.SetPixel(row, col, *red)
    for row in range(18, 20):
        for col in range(22, 26):
            matrix.SetPixel(row, col, *red)
    for row in range(28, 30):
        for col in range(22, 26):
            matrix.SetPixel(row, col, *red)
    for row in range(20, 22):
        for col in range(20, 22):
            matrix.SetPixel(row, col, *red)
    for row in range(26, 28):
        for col in range(20, 22):
            matrix.SetPixel(row, col, *red)



def main():
    # Pygame und COntrollerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick was
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Anzeige bei Beginn
    row = 0
    col = 0
    selection[row][col] = 1

    while True:
        clear_screen()
        draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Überprüfen der Joystick Eingaben
        # Verschieben nach rechts
        if joystick.get_axis(0) > 0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            if col < 1:
                selection[row][col] = 0
                col += 1
                selection[row][col] = 1
            elif col == 1:
                selection[row][col] = 0
                col = 0
                selection[row][col] = 1
        # Verschieben nach links
        elif joystick.get_axis(0) < -0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            if col > 0:
                selection[row][col] = 0
                col -= 1
                selection[row][col] = 1
            elif col == 0:
                selection[row][col] = 0
                col = 1
                selection[row][col] = 1
        # Verschieben nach oben
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) < -0.8:
            if row < 1:
                selection[row][col] = 0
                row += 1
                selection[row][col] = 1
            elif row == 1:
                selection[row][col] = 0
                row = 0
                selection[row][col] = 1
        # Verschieben nach unten
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) > 0.8:
            if row > 0:
                selection[row][col] = 0
                row -= 1
                selection[row][col] = 1
            elif row == 0:
                selection[row][col] = 0
                row = 1
                selection[row][col] = 1
        elif joystick.get_button(8) == 1:
            if selection[0][0] == 1:
                # links oben ausgewählt
                pass
            elif selection[0][1] == 1:
                # rechts oben ausgewählt
                pass
            elif selection[1][0] == 1:
                # links unten ausgewählt
                pass
            elif selection[1][1]:
                # Später hier den Aufruf für Tic-Tac-Toe hinzufügen
                pass

        pygame.time.Clock().tick(10)


main()
