import pygame
import sys
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# RGB-Matrix-Konfiguration
options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options=options)

# Größe des Quadrats und Schrittweite
square_size = 10
step_size = square_size

# Startposition des Quadrats
x_pos = 0
y_pos = 0

# Pygame initialisieren
pygame.init()

# Fenstergröße entsprechend der Matrixgröße setzen
screen = pygame.display.set_mode((options.cols, options.rows), pygame.DOUBLEBUF)

# Funktion zum Zeichnen des Quadrats auf der Matrix
def draw_square(x, y):
    matrix.Clear()
    matrix.SetPixel(x, y, 255, 0, 0)  # Setze Pixel auf Rot

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Quadrat bewegen
        if keys[pygame.K_RIGHT]:
            x_pos = (x_pos + 1) % 3
        elif keys[pygame.K_LEFT]:
            x_pos = (x_pos - 1) % 3
        elif keys[pygame.K_DOWN]:
            y_pos = (y_pos + 1) % 3
        elif keys[pygame.K_UP]:
            y_pos = (y_pos - 1) % 3

        # Quadrat zeichnen
        draw_square(x_pos * step_size, y_pos * step_size)

        time.sleep(0.1)  # Kurze Pause, um flüssige Bewegung sicherzustellen

except KeyboardInterrupt:
    pygame.quit()
