import numpy as np
import pygame
# importieren unserer Programme
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

SIZE = 1 # Größe 2
SIZE_FIELD = 16

# Leeres Array für die Pictogramme
selection = np.zeros((SIZE,SIZE), dtype = int)

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
    
    # Zeichnen der Piktogramme
    # Colorbattel
    for row in range(2, 7):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *red)
    for row in range(9, 14):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *blue)

    # tictactoe
    positions = [
        (17, 4), (18, 5), (19, 6), (20, 7), (21, 6), (22, 5), (23, 4), 
        (19, 8), (21, 8)
    ]
    
    # Zeichnen des X-Zeichens
    for pos in positions:
        matrix.SetPixel(pos[0], pos[1], *red)
    
    

# Anzeige der Auswahl
def display_screen():
    # Darstellung der Piktogramme
    for row in range(SIZE):
        for col in range(SIZE):
            color = (0, 0, 0)
            if selection[row][col] == 1:
                color = (255, 255, 255)
            for i in range(SIZE_FIELD - 1):
                matrix.SetPixel(row * SIZE_FIELD + i, col * SIZE_FIELD + i, *color)
                matrix.SetPixel((row + 1) * SIZE_FIELD + i, col * SIZE_FIELD + i, *color)
                matrix.SetPixel(row * SIZE_FIELD + i, (col + 1) * SIZE_FIELD + i, *color)

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
        #display_screen()

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
                    return
                    # Später hier ausschalten des Pi
        pygame.time.Clock().tick(10)
main()
