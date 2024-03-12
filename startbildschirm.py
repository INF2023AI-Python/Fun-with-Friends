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

# Startposition des orangenen Quadrats
orange_square_position = [0, 0]

def clear_screen():
    matrix.Clear()

def draw_screen():
    # Farbe der Linie (weiß)
    color = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    # Zeichnen der vertikalen Linie
    for row in range(32):
        matrix.SetPixel(0, row, *color)
    for row in range(32):
        matrix.SetPixel(15, row, *color)
    for row in range(32):
        matrix.SetPixel(31, row, *color)

    # Zeichnen der horizontalen Linie
    for col in range(32):
        matrix.SetPixel(col, 0, *color)
    for col in range(32):
        matrix.SetPixel(col, 15, *color)
    for col in range(32):
        matrix.SetPixel(col, 31, *color)

    # Zeichnen des orangefarbenen Rahmens um das ausgewählte Feld
    for row in range(SIZE):
        for col in range(SIZE):
            if selection[row][col] == 1:
                start_row = row * SIZE_FIELD
                end_row = (row + 1) * SIZE_FIELD
                start_col = col * SIZE_FIELD
                end_col = (col + 1) * SIZE_FIELD
                for r in range(start_row, end_row):
                    matrix.SetPixel(start_col, r, *red)  # linke Seite
                    matrix.SetPixel(end_col - 1, r, *red)  # rechte Seite
                for c in range(start_col, end_col):
                    matrix.SetPixel(c, start_row, *red)  # obere Seite
                    matrix.SetPixel(c, end_row - 1, *red)  # untere Seite

    # Zeichnen der Piktogramme innerhalb des ausgewählten Feldes
    for row in range(SIZE * SIZE_FIELD):
        for col in range(SIZE * SIZE_FIELD):
            # Beispielzeichnungen im Feld (können entsprechend angepasst werden)
            if row < 5 and col < 5:
                matrix.SetPixel(col + SIZE_FIELD // 2, row + SIZE_FIELD // 2, *red)  # Rotes Quadrat
            elif row > SIZE_FIELD - 6 and col < 5:
                matrix.SetPixel(col + SIZE_FIELD // 2, row + SIZE_FIELD // 2, *blue)  # Blaues Quadrat

def main():
    # Pygame und Controller-Initialisierung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick aus
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Anfangsposition des orangefarbenen Quadrats
    row = 0
    col = 0
    selection[row][col] = 1

    while True:
        clear_screen()
        draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Überprüfen der Joystick-Eingaben
        if joystick.get_axis(0) > 0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            if col < SIZE - 1:
                selection[row][col] = 0
                col += 1
                selection[row][col] = 1
        elif joystick.get_axis(0) < -0.8 and -0.2 < joystick.get_axis(1) < 0.2:
            if col > 0:
                selection[row][col] = 0
                col -= 1
                selection[row][col] = 1
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) < -0.8:
            if row < SIZE - 1:
                selection[row][col] = 0
                row += 1
                selection[row][col] = 1
        elif -0.2 < joystick.get_axis(0) < 0.2 and joystick.get_axis(1) > 0.8:
            if row > 0:
                selection[row][col] = 0
                row -= 1
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
            elif selection[1][1] == 1:
                # rechts unten ausgewählt
                return  # Hier kann der Pi heruntergefahren werden

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
