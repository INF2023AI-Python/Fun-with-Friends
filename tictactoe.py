import pygame
from pygame.locals import QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# RGB Matrix Konfiguration
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

# Startposition des Quadrats
x, y = 1, 1

# Bewegungsgeschwindigkeit
speed = 1

def draw_grid(canvas):
    for i in range(grid_size + 1):
        graphics.drawline(canvas, i * cell_size, 0, i * cell_size, grid_size * cell_size, graphics.Color(255, 255, 255))
        graphics.drawline(canvas, 0, i * cell_size, grid_size * cell_size, i * cell_size, graphics.Color(255, 255, 255))

def draw_square(canvas, x, y):
    graphics.rectangle(canvas, x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, graphics.Color(255, 165, 0))

# Pygame Konfiguration
pygame.init()
pygame.display.set_caption("LED Matrix Control")
screen = pygame.display.set_mode((320, 320))  # Passende Größe für das 32x32 Gitter

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP] and y > 0:
        y -= speed
    elif keys[K_DOWN] and y < grid_size - 1:
        y += speed
    elif keys[K_LEFT] and x > 0:
        x -= speed
    elif keys[K_RIGHT] and x < grid_size - 1:
        x += speed

    # Gitter zeichnen
    canvas = matrix.CreateFrameCanvas()
    draw_grid(canvas)

    # Quadrat zeichnen
    draw_square(canvas, x, y)

    canvas = matrix.SwapOnVSync(canvas)

    time.sleep(0.05)  # Kurze Verzögerung für die Sichtbarkeit der Bewegung

pygame.quit()
