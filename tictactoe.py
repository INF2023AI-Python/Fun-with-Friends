import time
import pygame
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# RGBMatrix-Optionen
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

line_color = (255, 255, 255)  # weiß

font = pygame.font.Font(None, 36)
game_over = False

cell_width = matrix.width // 6
cell_height = matrix.height // 6

game_board = [['', '', ''],
              ['', '', ''],
              ['', '', '']]

def draw_grid(surface):
    for i in range(1, 3):
        pygame.draw.line(surface, line_color, (i * cell_width, 0), (i * cell_width, matrix.height // 2), 5)

    for i in range(1, 3):
        pygame.draw.line(surface, line_color, (0, i * cell_height), (matrix.width // 2, i * cell_height), 5)

def draw_xo(surface):
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == 'X':
                pygame.draw.line(surface, line_color, (col * cell_width, row * cell_height),
                                 ((col + 1) * cell_width, (row + 1) * cell_height), 2)
                pygame.draw.line(surface, line_color, ((col + 1) * cell_width, row * cell_height),
                                 (col * cell_width, (row + 1) * cell_height), 2)
            elif game_board[row][col] == 'O':
                pygame.draw.circle(surface, line_color, (col * cell_width + cell_width // 2,
                                                         row * cell_height + cell_height // 2),
                                   cell_width // 2, 2)

def player_turn(surface):
    text = font.render('Player: ' + turn + ' ', True, (0, 0, 0), (255, 255, 255))
    surface.blit(text, (100, cell_height * 4))

def check_winner():
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != '':
            return game_board[i][0]
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != '':
            return game_board[0][i]

    if game_board[0][0] == game_board[1][1] == game_board[2][2] != '':
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != '':
        return game_board[0][2]

    return None

# Hauptprogrammschleife
turn = 'X'
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // (matrix.height // 6)
            clicked_col = mouseX // (matrix.width // 6)

            if game_board[clicked_row][clicked_col] == '':
                game_board[clicked_row][clicked_col] = turn
                if turn == 'X':
                    turn = 'O'
                else:
                    turn = 'X'

    game_surface = pygame.Surface((matrix.width, matrix.height))
    game_surface.fill((0, 0, 0))
    draw_grid(game_surface)
    player_turn(game_surface)
    draw_xo(game_surface)

    pygame.surfarray.blit_array(matrix, pygame.surfarray.array3d(game_surface))
    pygame.display.flip()

    winner = check_winner()
    if winner:
        game_over = True
        print('Winner:', winner)
    elif all(game_board[i][j] != '' for i in range(3) for j in range(3)):
        game_over = True
        print('DRAW')

pygame.quit()
sys.exit()
