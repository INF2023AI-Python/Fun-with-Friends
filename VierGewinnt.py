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

# Konfiguration der Matrix
options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)

# Funktion zum Löschen des Spielfelds
def clear_screen():
    matrix.Clear()

# Anzeigen des Spielfelds
def display_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = (0,0,0) # Ausschlten leerer Zellen
            if board[row][col] == 1:
                color = (255, 0, 0) # Spieler 1: Rot
            elif board[row][col] == 2:
                color = (0, 0, 255) # Spieler 2: Blau
            for i in range(CHIP_SIZE):
                for j in range(CHIP_SIZE):
                    matrix.SetPixel(col * CHIP_SIZE + j + 6, row * CHIP_SIZE + i + 8, *color)
                    
# Funktion zum Prüfen auf Gewinn
def check_win(player):
    # Horizontale Linie
    for r in range(ROWS):
        for c in range(COLS - 3): 
            if all(board[r][c + i] == player for i in range(3)):
                return True
            
    # Vertikale Linie
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(3)):
                return True
        
    # Diagonal nach oben rechts
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(3)):
                return True
            
    # Diagonale nach unten rechts
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(3)):
                return True
            
    return False

# AUf Unentschieden Prüfen
def check_draw():
    for c in range(COLS):
        if all(board[2][c] != 0):
            return True
    return False



class RunText:
    def __init__(self, matrix, win_text, player_text, symbol_text):
        self.matrix = matrix
        self.win_text = win_text
        self.player_text = player_text
        self.symbol_text = symbol_text
        self.text_color = self.determine_text_color()

    def determine_text_color(self):
        if self.symbol_text == 1:
            return graphics.Color(255, 0, 0)  # Rot für Spieler 1
        elif self.symbol_text == 2:
            return graphics.Color(0, 0, 255)  # Blau für Spieler 2
        else:
            return graphics.Color(255, 255, 255)  # Weiß für Unentschieden

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

        # Ersetze die Zeilen, die die Breite berechnen
        win_text_width = graphics.DrawText(offscreen_canvas, font, 0, 0, self.text_color, self.win_text)
        player_text_width = graphics.DrawText(offscreen_canvas, font, 0, 0, self.text_color, self.player_text)
        symbol_text_width = graphics.DrawText(offscreen_canvas, font, 0, 0, self.text_color, str(self.symbol_text))

        # Zentriere den Text horizontal
        text_x = (offscreen_canvas.width - max(win_text_width, player_text_width, symbol_text_width)) // 2

        # Zentriere den Text vertikal
        text_y = (offscreen_canvas.height - 3 * font.height) // 2

        # Verschiebe den Text, um ihn besser im Raster zu zentrieren
        text_x += 2  # Beispielwert, passen Sie dies nach Bedarf an
        text_y += 2  # Beispielwert, passen Sie dies nach Bedarf an

        while True:
            offscreen_canvas.Clear()

            # Zeige den Win-Text an
            graphics.DrawText(offscreen_canvas, font, text_x, text_y, self.text_color, self.win_text)            
            # Zeige den Player-Text an
            graphics.DrawText(offscreen_canvas, font, text_x, text_y + font.height, self.text_color, self.player_text)
            # Zeige den Symbol-Text an
            graphics.DrawText(offscreen_canvas, font, text_x, text_y + 2 * font.height, self.text_color, str(self.symbol_text))

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            time.sleep(5)
            break



def display_winner(player):
    if player == 1:
        win_text = "WIN"
        player_text = f"Player {player}"
        symbol_text = player
        run_text = RunText(matrix, win_text, player_text, symbol_text)
        run_text.run()
        time.sleep(5)
    if player == 2:
        matrix.Fill(0, 0, 255)
        time.sleep(5)

def vierGewinnt():
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

    #Anzeige des Chips vor Spielbeginn
    player = 1
    col = 0
    board[0][col] = 1

    while True:
        clear_screen()
        display_board()

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
                        if row > 2:
                            board[row][col] = player
                            break
                # Überprüfen auf Gewinn
                if check_win(player):
                    clear_screen()
                    display_winner(player)
                    return
                # Spielerwechsel
                player = 2 if player == 1 else 1
                if check_draw():
                    clear_screen()
                    #display_draw()
                    return
        pygame.time.Clock().tick(7)

if __name__ == "__main__":
    vierGewinnt()
