import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

orange_square_position = [0, 0]

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
def draw_screen(x, y):
    # Farbe der Linie (weiß)
    color = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    orange = (255, 165, 0)  # Orange Farbe

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

    # Position des Quadrats anpassen
    x_pos = int(x * 15)  # Skalierung der Joystick-Achsen auf 0-15
    y_pos = int(y * 15)

    # Zeichnen der orangefarbenen Linien
   # Obere Linie
    if x_pos % 2 == 0 and y_pos % 2 == 0:  # Wenn beide gerade sind
        for i in range(16):
            matrix.SetPixel(i + x_pos * 16, y_pos * 16, *orange)
    elif x_pos % 2 == 1 and y_pos % 2 == 0:  # Wenn x_pos ungerade ist und y_pos gerade
        for i in range(16):
            matrix.SetPixel(i + x_pos * 16 - 16, y_pos * 16, *orange)
    else:  # Wenn x_pos gerade ist und y_pos ungerade oder beide ungerade sind
        for i in range(16):
            matrix.SetPixel(i + x_pos * 16, y_pos * 16 - 16, *orange)
    
    # Untere Linie
    for i in range(16):
        matrix.SetPixel(i + x_pos * 16, 15 + y_pos * 16, *orange)
    
    # Linke Linie
    for i in range(16):
        matrix.SetPixel(x_pos * 16, i + y_pos * 16, *orange)
    
    # Rechte Linie
    for i in range(16):
        matrix.SetPixel(15 + x_pos * 16, i + y_pos * 16, *orange) 
       
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
    for row in range(22, 24):  # Decrease starting and ending row values by 1
        for col in range(17, 23):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(21, 25):  # Decrease starting and ending row values by 1
        for col in range(27, 29):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(19, 21):  # Decrease starting and ending row values by 1
        for col in range(25, 27):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(25, 27):  # Decrease starting and ending row values by 1
        for col in range(25, 27):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(17, 19):  # Decrease starting and ending row values by 1
        for col in range(21, 25):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(27, 29):  # Decrease starting and ending row values by 1
        for col in range(21, 25):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(19, 21):  # Decrease starting and ending row values by 1
        for col in range(19, 21):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)
    for row in range(25, 27):  # Decrease starting and ending row values by 1
        for col in range(19, 21):  # Shift left by one pixel
            matrix.SetPixel(row, col, *red)

def update_orange_square_position(orange_square_position, joystick):
    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Bewegungsrichtung basierend auf den Achsenwerten mit Toleranz
    if -0.2 < x_axis < 0.2 and y_axis < -0.8:
        # Bewege nach oben
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] - 1))]
        print("Bewege nach oben")
    elif -0.2 < x_axis < 0.2 and y_axis > 0.8:
        # Bewege nach unten
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] + 1))]
        print("Bewege nach unten")
    elif x_axis > 0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach rechts
        new_position = [max(0, min(1, orange_square_position[0] + 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Bewege nach rechts")
    elif x_axis < -0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach links
        new_position = [max(0, min(1, orange_square_position[0] - 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Bewege nach links")
    else:
        # Keine Bewegung, wenn keine der Bedingungen erfüllt ist
        new_position = orange_square_position

    # Rückgabe der neuen Position
    return new_position

def main():
    global orange_square_position
    # Pygame und Controllerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick was
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    running = True
    while running:
        clear_screen()
        # Rufe update_orange_square_position auf, um die Position des orangen Quadrats zu aktualisieren
        orange_square_position = update_orange_square_position(orange_square_position, joystick)
        # Übergebe die aktualisierte Position an draw_screen
        draw_screen(orange_square_position[0], orange_square_position[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
