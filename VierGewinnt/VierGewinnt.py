import time
import numpy as np
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import sys

# Angaben zum Spielfeld
ROWS = 8 #Zeile 2 ist der Abstand zwischen Feld und der Auswahl der Spalte
COLS = 7 
CHIP_SIZE = 3

# Leeres Array für das Spielfeld
board = np.zeros((ROWS, COLS), dtype=int)


# Anzeigen des Spielfelds
def display_board(offset_canvas, matrix):
    for row in range(ROWS):
        for col in range(COLS):
            color = (0,0,0) # Ausschlten leerer Zellen
            if board[row][col] == 1:
                color = (255, 0, 0) # Spieler 1: Rot
            elif board[row][col] == 2:
                color = (0, 0, 255) # Spieler 2: Blau
            for i in range(CHIP_SIZE):
                for j in range(CHIP_SIZE):
                    offset_canvas.SetPixel(col * CHIP_SIZE + j + 6, row * CHIP_SIZE + i + 8, *color)
    return matrix.SwapOnVSync(offset_canvas)
                    
# Funktion zum Prüfen auf Gewinn
def check_win(player):
    # Horizontale Linie
    for r in range(ROWS):
        for c in range(COLS - 3): 
            if all(board[r][c + i] == player for i in range(4)):
                return True
            
    # Vertikale Linie
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
        
    # Diagonal nach oben rechts
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
            
    # Diagonale nach unten rechts
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
            
    return False

# AUf Unentschieden Prüfen
def check_draw():
    for c in range(COLS):
        if board[2][c] == 0:
            return False
    return True

# Funktion zum Erstellen eines Canvas und Anzeigen des Texts
def display_text(text, color, offset_canvas, matrix):
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

# Darstellung Gewinnbildschirm
def display_winner(player, offset_canvas, matrix):
    if player == 1:
        color = (255, 0, 0)
        display_text(["WIN", "Player", "1"], color, offset_canvas, matrix)
        time.sleep(5)
    if player == 2:
        color = (0, 0, 255)
        display_text(["WIN", "Player2", "2"], color, offset_canvas, matrix)
        time.sleep(5)

# Darstellung bei unentschieden
def display_draw(offset_canvas, matrix):
    color = (255, 255, 255)
    display_text(["DRAW", " ", " "], color, offset_canvas, matrix)
    time.sleep(5)

def vierGewinnt(offset_canvas, matrix):
    # Pygame und COntrollerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick aus
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    #Anzeige des Chips vor Spielbeginn
    player = 1
    col = 0
    board[0][col] = 1

    while True:
        matrix.Clear()
        offset_canvas = display_board(offset_canvas, matrix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # x_axis = joystick.get_axis(0)
        #y_axis = joystick.get_axis(1)

        # Überprüfen der Joystick Eingaben
            # Verschieben nach rechts
            elif joystick.get_axis(0) > 0.8 and -0.2 < joystick.get_axis(1) < 0.2:
                if col < 6:
                    board[0][col] = 0
                    col += 1
                    board[0][col] = player
                elif col == 6:
                    board[0][col] = 0
                    col = 0
                    board[0][col] = player
            # Verschieben nach links
            elif joystick.get_axis(0) < -0.8 and -0.2 < joystick.get_axis(1) < 0.2:
                if col > 0:
                    board[0][col] = 0
                    col -= 1
                    board[0][col] = player
                elif col == 0:
                    board[0][col] = 0
                    col = 6
                    board[0][col] = player
            #Bestätigen der Eingabe, Umstellen auf anderen Button, um zweifach Eingabe zu verhindern
            elif joystick.get_button(1) == 1:
                # Finden der nächsten freien Zeile
                for row in range(ROWS - 1, 0, -1):
                    if board[row][col] == 0:
                        if row > 1:
                            for move in range(2, row +1):
                                board[move - 1][col] = 0
                                board[move][col] = player
                                time.sleep(0.25)
                                offset_canvas = display_board(offset_canvas, matrix)
                            break
                        else:
                            player = 2 if player == 1 else 1
                            break

                # Überprüfen auf Gewinn
                if check_win(player):
                    matrix.Clear()
                    display_winner(player, offset_canvas, matrix)
                    return
                
                # Überprüfen auf Untentschieden
                if check_draw():
                    matrix.Clear()
                    display_draw(offset_canvas, matrix)
                    return
                
                # Spielerwechsel
                player = 2 if player == 1 else 1
                board[0][col] = player
                
        pygame.time.Clock().tick(7)
