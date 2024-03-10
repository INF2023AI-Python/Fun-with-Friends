import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
from pygame.locals import KEYDOWN, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0

matrix = RGBMatrix(options=options)

# Gitterparameter
grid_size = 3
cell_size = 10

# Startposition des orangenen Quadrats
orange_square_position = [1, 1]

# Bewegungsgeschwindigkeit des orangenen Quadrats
speed = 1

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    for row in range(32):
        for col in range(32):
            # Zeichne das Raster
            if row % 10 == 0 or col % 10 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

def draw_square(orange_square_position):
    x1, y1, x2, y2 = orange_square_position[0] * 10, orange_square_position[1] * 10, (orange_square_position[0] + 1) * 10, (orange_square_position[1] + 1) * 10
    for x in range(x1, x2):
        for y in range(y1, y2):
            matrix.SetPixel(x, y, 255, 165, 0)

# Funktion zum Aktualisieren der Position des orangenen Quadrats basierend auf den Tasteneingaben
def update_square_position():
    global orange_square_position

    keys = pygame.key.get_pressed()
    if keys[K_UP] and orange_square_position[1] > 0:
        orange_square_position[1] -= speed
    elif keys[K_DOWN] and orange_square_position[1] < grid_size - 1:
        orange_square_position[1] += speed
    elif keys[K_LEFT] and orange_square_position[0] > 0:
        orange_square_position[0] -= speed
    elif keys[K_RIGHT] and orange_square_position[0] < grid_size - 1:
        orange_square_position[0] += speed

# Hauptspiel-Schleife
while True:
    pygame.init()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                update_square_position()

    draw_board()
    draw_square(orange_square_position)

    pygame.time.Clock().tick(10)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen
