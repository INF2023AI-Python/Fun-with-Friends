#!/usr/bin/env python3
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import pygame
import sys

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

# Funktion zum Zeichnen des Tictactoe-Boards auf der RGB-LED-Matrix
def draw_board():
    matrix.Clear()
    for row in range(1, 32, 10):
        graphics.DrawLine(matrix, 0, row, 30, row, graphics.Color(100, 100, 100))
        graphics.DrawLine(matrix, row, 0, row, 30, graphics.Color(100, 100, 100))

# Initialisiere die Position des Quadrats
square_x, square_y = 0, 0

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    sys.exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Button 0 drücken (nach oben bewegen)
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            square_y = max(square_y - 1, 0)

        # Button 1 drücken (nach rechts bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 1:
            square_x = min(square_x + 1, 2)

        # Button 2 drücken (nach unten bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
            square_y = min(square_y + 1, 2)

        # Button 3 drücken (nach links bewegen)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 3:
            square_x = max(square_x - 1, 0)

        # Button 5 drücken (Bestätigung)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 5:
            print(f"Selected cell: ({square_x}, {square_y})")

    # Tic-Tac-Toe-Board und Quadrat zeichnen
    draw_board()
    graphics.DrawLine(matrix, square_x * 10, square_y * 10, (square_x + 1) * 10, square_y * 10, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, square_x * 10, square_y * 10, square_x * 10, (square_y + 1) * 10, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, (square_x + 1) * 10, square_y * 10, (square_x + 1) * 10, (square_y + 1) * 10, graphics.Color(255, 0, 0))
    graphics.DrawLine(matrix, square_x * 10, (square_y + 1) * 10, (square_x + 1) * 10, (square_y + 1) * 10, graphics.Color(255, 0, 0))

    time.sleep(0.1)  # Fügt eine kurze Verzögerung hinzu, um die Bewegung sichtbar zu machen
