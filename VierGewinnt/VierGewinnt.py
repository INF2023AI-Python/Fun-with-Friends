import time
import numpy as np
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import sys

# Size of the board
ROWS = 8 # 2nd row is empty (distance between board and selection)
COLS = 7 
CHIP_SIZE = 3

# Empty array for the board
board = np.zeros((ROWS, COLS), dtype=int)


# Displaying the board on the matrix
def display_board(offset_canvas, matrix):
    for row in range(ROWS):
        for col in range(COLS):
            color = (0,0,0) # Turning off empty cells
            if board[row][col] == 1:
                color = (255, 0, 0) # Player 1: Red
            elif board[row][col] == 2:
                color = (0, 0, 255) # Player 2: Blue
            for i in range(CHIP_SIZE):
                for j in range(CHIP_SIZE):
                    offset_canvas.SetPixel(col * CHIP_SIZE + j + 6, row * CHIP_SIZE + i + 8, *color)
    return matrix.SwapOnVSync(offset_canvas)
                    
# Check for winner
def check_win(player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3): 
            if all(board[r][c + i] == player for i in range(4)):
                return True
            
    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
        
    # Diagonal (top right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
            
    # Diagonal (bottom right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
            
    return False

# Check for draw
def check_draw():
    for c in range(COLS):
        if board[2][c] == 0:
            return False
    return True

# Displaying text in the matrix
def display_text(text, color, offset_canvas, matrix):
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
    textColor = graphics.Color(*color)

    # Text in the first line
    graphics.DrawText(offset_canvas, font, 2, 10, textColor, text[0])
    # Text in the second line
    graphics.DrawText(offset_canvas, font, 2, 20, textColor, text[1])
    # Text in the third line
    graphics.DrawText(offset_canvas, font, 2, 30, textColor, text[2])

    matrix.SwapOnVSync(offset_canvas)

# Displaying the winner
def display_winner(player, offset_canvas, matrix):
    if player == 1:
        color = (255, 0, 0)
        display_text(["WIN", "Player", "1"], color, offset_canvas, matrix)
        time.sleep(5)
    if player == 2:
        color = (0, 0, 255)
        display_text(["WIN", "Player2", "2"], color, offset_canvas, matrix)
        time.sleep(5)

# Displaying a draw
def display_draw(offset_canvas, matrix):
    color = (255, 255, 255)
    display_text(["DRAW", " ", " "], color, offset_canvas, matrix)
    time.sleep(5)

# Main game
def vierGewinnt(offset_canvas, matrix):
    # Starting pygame and checking available controllers
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Select the first available joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Displaying the chip at the beginning of the game
    player = 1
    col = 0
    board[0][col] = 1

    while True:
        matrix.Clear()
        offset_canvas = display_board(offset_canvas, matrix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # CHecking the controller input
            # Moving the chip to the right
            elif joystick.get_axis(0) > 0.8 and -0.2 < joystick.get_axis(1) < 0.2:
                if col < 6:
                    board[0][col] = 0
                    col += 1
                    board[0][col] = player
                elif col == 6:
                    board[0][col] = 0
                    col = 0
                    board[0][col] = player
            # Moving the Chip to the left
            elif joystick.get_axis(0) < -0.8 and -0.2 < joystick.get_axis(1) < 0.2:
                if col > 0:
                    board[0][col] = 0
                    col -= 1
                    board[0][col] = player
                elif col == 0:
                    board[0][col] = 0
                    col = 6
                    board[0][col] = player
            # Selesting the column to place the chip
            elif joystick.get_button(1) == 1:
                # Searching the next available row for the chip
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

                # Checking for a win
                if check_win(player):
                    matrix.Clear()
                    display_winner(player, offset_canvas, matrix)
                    matrix.Clear()
                    return
                
                # Checking for a draw
                if check_draw():
                    matrix.Clear()
                    display_draw(offset_canvas, matrix)
                    matrix.Clear()
                    return
                
                # Changing the player
                player = 2 if player == 1 else 1
                board[0][col] = player
                
        pygame.time.Clock().tick(7)
