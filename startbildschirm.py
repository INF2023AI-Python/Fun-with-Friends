import numpy as np
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

SIZE = 1  # Größe 2
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


def clear_screen():
    matrix.Clear()


def draw_orange_square(row, col):
    # Farbe des Quadrats (orange)
    color = (255, 165, 0)

    # Position und Größe des Quadrats
    start_row = row
    end_row = row + 5
    start_col = col
    end_col = col + 5

    # Zeichnen des orangefarbenen Quadrats
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            matrix.SetPixel(c, r, *color)


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
    # Pygame und Controllerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Anfangsposition des orangefarbenen Quadrats
    orange_row = 5
    orange_col = 5

    while True:
        clear_screen()
        draw_screen()

        # Bewegung des orangefarbenen Quadrats basierend auf Joystick-Eingaben
        if joystick.get_axis(0) > 0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            orange_col += 1
        elif joystick.get_axis(0) < -0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            orange_col -= 1
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) < -0.8:
            orange_row -= 1
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) > 0.8:
            orange_row += 1

        # Grenzen für die Position des orangefarbenen Quadrats sicherstellen
        orange_row = max(0, min(orange_row, 26))
        orange_col = max(0, min(orange_col, 26))

        # Zeichnen des orangefarbenen Quadrats
        draw_orange_square(orange_row, orange_col)

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
