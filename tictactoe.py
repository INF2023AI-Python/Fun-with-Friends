import time
import pygame
from pygame.locals import QUIT
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

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

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    matrix.Clear()
    for row in range(32):
        for col in range(32):
            # Zeichne das Raster
            if row % 10 == 0 or col % 10 == 0:
                matrix.SetPixel(col, row, 100, 100, 100)

def draw_square(orange_square_position):
    x1, y1, x2, y2 = orange_square_position[0] * 10, orange_square_position[1] * 10, (orange_square_position[0] + 1) * 10, (orange_square_position[1] + 1) * 10

    # Zeichne den Rahmen des Quadrats
    graphics.DrawLine(matrix, x1, y1, x2, y1, graphics.Color(255, 165, 0))  # Obere Linie
    graphics.DrawLine(matrix, x2, y1, x2, y2, graphics.Color(255, 165, 0))  # Rechte Linie
    graphics.DrawLine(matrix, x2, y2, x1, y2, graphics.Color(255, 165, 0))  # Untere Linie
    graphics.DrawLine(matrix, x1, y2, x1, y1, graphics.Color(255, 165, 0))  # Linke Linie

# Funktion zum Aktualisieren der Position des orangenen Quadrats basierend auf den Achsen des Joysticks
def update_square_position(joystick):
    global orange_square_position

    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Aktualisiere die Position des orangenen Quadrats basierend auf den Achsenwerten
    new_position = [max(0, min(grid_size - 1, orange_square_position[0] + int(x_axis))),
                    max(0, min(grid_size - 1, orange_square_position[1] - int(y_axis)))]

    # Überprüfe, ob die neue Position frei ist
    if matrix.GetPixel(new_position[0] * 10, new_position[1] * 10) != (255, 165, 0):
        orange_square_position = new_position

# Hauptspiel-Schleife
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    draw_board()
    update_square_position(joystick)
    draw_square(orange_square_position)

    time.sleep(0.1)  # Fügt eine Verzögerung hinzu, um das Board besser sichtbar zu machen
