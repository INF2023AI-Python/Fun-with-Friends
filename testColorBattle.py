import time
import numpy as np
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import sys

options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Angaben zum Spielfeld
FIELDS = 15 #16 mit 0
PLAYER_SIZE = 2

# Leeres Array für das Spielfeld
field = np.zeros((FIELDS, FIELDS), dtype=int)

# Anzeigen des Spielfelds
def display_field(offset_canvas, matrix):
    for row in range(FIELDS):
        for col in range(FIELDS):
            color = (0, 0, 0)
            if field[row][col] == 1:
                color = (255, 0, 0) # Spiler 1: Rot
            elif field[row][col] == 2:
                color = (0, 0, 255) # Spieler 2: Blau
            for i in range(PLAYER_SIZE):
                for j in range(PLAYER_SIZE):
                    offset_canvas.SetPixel(row * PLAYER_SIZE + i, col * PLAYER_SIZE + j, *color)
    return matrix.SwapOnVSync(offset_canvas)

# Funktion zum Erstellen eines Canvas und Anzeigen des Texts
def display_winner(text, color, offset_canvas, matrix):
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
    textColor = graphics.Color(*color)

    # Zeige den Text der ersten Zeile an
    graphics.DrawText(offset_canvas, font, 2, 10, textColor, text[0])
    # Zeige den Text der zweiten Zeile an
    graphics.DrawText(offset_canvas, font, 2, 20, textColor, text[1])
    # Zeige den Text der dritte Zeile an
    graphics.DrawText(offset_canvas, font, 2, 30, textColor, text[2])

    matrix.SwapOnVSync(offset_canvas)

# Prüfen auf Gewinner
def check_winner(offset_canvas, matrix):
    counter1 = 0
    counter2 = 0
    for r in range(FIELDS):
        for c in range(FIELDS):
            if field[r][c] == 1:
                counter1 += 1
            elif field[r][c] == 2:
                counter2 += 1
    if counter1 > counter2:
        color = (255, 0, 0)
        display_winner(["WIN", "Player", "1"], color, offset_canvas, matrix)
    elif counter1 < counter2:
        color = (0, 0, 255)
        display_winner(["WIN", "Player", "2"], color, offset_canvas, matrix)
    elif counter1 == counter2:
        color = (255, 255, 255)
        display_winner(["DRAW", " ", " "], color, offset_canvas, matrix)

# Hauptspiel
def ColorBattle(offset_canvas, matrix):
    pygame.init()
    pygame.joystick.init()

    # Überprüfen, ob Joysticks vorhanden sind
    if pygame.joystick.get_count() < 2:
        print("Nicht genügend Joysticks gefunden.")
        pygame.quit()
        quit()

    # Initialisieren der Joysticks
    joystick1 = pygame.joystick.Joystick(0)
    joystick2 = pygame.joystick.Joystick(1)

    # Starten der Joysticks
    joystick1.init()
    joystick2.init()

    # Anzeige der Spieler vor Spielbeginn
    row1 = 0
    col1 = 0
    field[row1][col1] = 1
    row2 = 0
    col2 = 15
    field[row2][col2] = 2

    # Zeit zum Spielbeginn
    time_threshold = 60
    start_time = time.time()

    while True:
        matrix.Clear()
        # Aktuelle Zeit abrufen
        current_time = time.time()
    
        # Zeitdifferenz berechnen
        elapsed_time = current_time - start_time

        # Hauptereignisschleife
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Überprüfen der Eingaben für Spieler 1
            # Verschieben nach rechts
            elif joystick1.get_axis(0) > 0.8 and -0.2 < joystick1.get_axis(1) < 0.2:
                if col1 < 15:
                    col1 += 1
                    field[row1][col1] = 1
                    offset_canvas = display_field(offset_canvas, matrix)
                elif col1 == 15:
                    col1 = 15
                    field[row1][col1] = 1
            # Verschieben nach links
            elif joystick1.get_axis(0) < -0.8 and -0.2 < joystick1.get_axis(1) < 0.2:
                if col1 > 0:
                    col1 -= 1
                    field[row1][col1] = 1
                    offset_canvas = display_field(offset_canvas, matrix)
                elif col1 == 0:
                    col1 = 0
                    field[row1][col1] = 1
            # Verschieben nach oben
            elif joystick1.get_axis(1) < -0.8 and -0.2 < joystick1.get_axis(0) < 0.2:
                if row1 < 15:
                    row1 += 1
                    field[row1][col1] = 1
                    offset_canvas = display_field(offset_canvas, matrix)
                elif row1 == 15:
                    row1 = 15
                    field[row1][col1] = 1
            # Verschieben nach links
            elif joystick1.get_axis(1) > 0.8 and -0.2 < joystick1.get_axis(0) < 0.2:
                if row1 > 0:
                    row1 -= 1
                    field[row1][col1] = 1
                    offset_canvas = display_field(offset_canvas, matrix)
                elif row1 == 0:
                    row1 = 0
                    field[row1][col1] = 1
        
        # Überprüfen der Eingaben für Spieler 2
            # Verschieben nach rechts
            elif joystick2.get_axis(0) > 0.8 and -0.2 < joystick2.get_axis(1) < 0.2:
                if col2 < 15:
                    col2 += 1
                    field[row2][col2] = 2
                    offset_canvas = display_field(offset_canvas, matrix)
                elif col2 == 15:
                    col2 = 15
                    field[row2][col2] = 2
            # Verschieben nach links
            elif joystick2.get_axis(0) < -0.8 and -0.2 < joystick2.get_axis(1) < 0.2:
                if col2 > 0:
                    col2 -= 1
                    field[row2][col2] = 2
                    offset_canvas = display_field(offset_canvas, matrix)
                elif col2 == 0:
                    col2 = 0
                    field[row2][col2] = 2
            # Verschieben nach oben
            elif joystick2.get_axis(1) < -0.8 and -0.2 < joystick2.get_axis(0) < 0.2:
                if row2 < 15:
                    row2 += 1
                    field[row2][col2] = 2
                    offset_canvas = display_field(offset_canvas, matrix)
                elif row2 == 15:
                    row2 = 15
                    field[row2][col2] = 2
            # Verschieben nach links
            elif joystick2.get_axis(1) > 0.8 and -0.2 < joystick2.get_axis(0) < 0.2:
                if row2 > 0:
                    row2 -= 1
                    field[row2][col2] = 1
                    offset_canvas = display_field(offset_canvas, matrix)
                elif row2 == 0:
                    row2 = 0
                    field[row2][col2] = 2
        
        # Gewinner prüfen, wenn Zeit um ist
        if elapsed_time >= time_threshold:
            matrix.Clear()
            check_winner(offset_canvas, matrix)
            matrix.Clear()
            return
        
if __name__ == "__main__":
    ColorBattle()
                