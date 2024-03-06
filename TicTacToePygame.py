#from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
#from samplebase import SampleBase
import pygame
import sys


pygame.init()

#Configuration for the matrix
# options = RGBMatrixOptions()
# options.rows = 32
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = 'adafruit-hat'# Important don't forget

# matrix = RGBMatrix(options = options)

# offset_canvas = matrix.CreateFrameCanvas()

#screen Eigenschaften
window_width = 320
window_height = 320
window = pygame.display.set_mode((window_width, window_height))

line_color = (255, 255, 255) #weiß

#Text Eigenschaften
font = pygame.font.Font(None, 36)
game_over = False

#Gridlinen Größe
cell_width = window_width // 6
cell_height = window_height // 6

game_board = [['', '', ''],
              ['', '', ''],
              ['', '', '']]

#RGBMatrixEmulator
# for i in range(1, 3):
#     for y in range(16):
#         offset_canvas.SetPixel(i * 5, y, 255, 255, 255)
#         offset_canvas = matrix.SwapOnVSync(offset_canvas)

# for i in range(1, 3):
#     for x in range(16):
#         offset_canvas.SetPixel(x, i * 5, 255, 255, 255)
#         offset_canvas = matrix.SwapOnVSync(offset_canvas)



def draw_grid():
    
    # Vertikale Linien
    for i in range(1, 3):
        pygame.draw.line(window, line_color, ( i * cell_width, 0), (i * cell_width, window_height // 2), 5)

    # Horizontale Linien
    for i in range(1, 3):
        pygame.draw.line(window, line_color, (0, i * cell_height), (window_width // 2, i * cell_height), 5)

def draw_xo():
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == 'X':
                pygame.draw.line(window, line_color, (col * cell_width, row * cell_height), 
                                 ((col + 1) * cell_width, (row + 1) * cell_height), 2)
                pygame.draw.line(window, line_color,((col + 1) * cell_width, row * cell_height), 
                                 (col * cell_width, (row + 1) * cell_height), 2)
            elif game_board[row][col] == 'O':
                pygame.draw.circle(window, line_color, (col * cell_width + cell_width // 2, row * cell_height + cell_height // 2), 
                                   cell_width // 2, 2)

def player_turn():
    text = font.render('Player: ' + turn + ' ', True, 0,0,0, 250,250,250)
    window.blit(text, (100, cell_height * 4))

#graphics.DrawText(offset_canvas, font, 2, 10, line_color, "Player: ")

def check_winner():
    for i in range(3):
        if game_board[i][0] == game_board [i][1] == game_board[i][2] != '':
            return game_board[i][0]
        if game_board[0][i] == game_board [1][i] == game_board[2][i] != '':
            return game_board[0][i]
        
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != '':
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != '':
        return game_board[0][2]

    return None


#Hauptprogrammschleife
turn = 'X'
running = True    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running  = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // (window_height // 6)
            clicked_col = mouseX // (window_width // 6)
            
            if game_board[clicked_row][clicked_col] == '':
                game_board[clicked_row][clicked_col] = turn
                if turn == 'X':
                    turn = 'O'                   
                else:
                    turn = 'X'

        

    draw_grid()
    player_turn()
    draw_xo()

    winner = check_winner()
    if winner:
        game_over = True
        text = font.render('Winner: ' + winner, True, 0,0,0, 250,250,250)
        window.blit(text, (100, cell_height * 4))
    elif all(game_board[i][j] != '' for i in range(3) for j in range(3)):
        game_over = True
        text = font.render('   DRAW   ', True, 0,0,0, 250,250,250)
        window.blit(text, (100, cell_height * 4))

    pygame.display.flip()

pygame.quit()
sys.exit()
