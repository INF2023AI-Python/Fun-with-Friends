import pygame
import sys

pygame.init()

# screen Eigenschaften
window_width = 320
window_height = 320
window = pygame.display.set_mode((window_width, window_height))

line_color = (255, 255, 255)  # weiß
line_color1 = (0, 0, 0)

# Text Eigenschaften
font = pygame.font.Font(None, 36)
game_over = False

# Gridlinen Größe
cell_width = window_width // 6
cell_height = window_height // 6

game_board = [['', '', ''],
              ['', '', ''],
              ['', '', '']]

# Variable für die ausgewählte Position
selected_row, selected_col = 0, 0

# Initialisiere die Joysticks außerhalb der Schleife
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

def draw_grid():
    # Vertikale Linien
    for i in range(1, 3):
        pygame.draw.line(window, line_color, (i * cell_width, 0), (i * cell_width, window_height // 2), 5)

    # Horizontale Linien
    for i in range(1, 3):
        pygame.draw.line(window, line_color, (0, i * cell_height), (window_width // 2, i * cell_height), 5)

def draw_xo():
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == 'X':
                pygame.draw.line(window, line_color, (col * cell_width, row * cell_height),
                                 ((col + 1) * cell_width, (row + 1) * cell_height), 2)
                pygame.draw.line(window, line_color, ((col + 1) * cell_width, row * cell_height),
                                 (col * cell_width, (row + 1) * cell_height), 2)
            elif game_board[row][col] == 'O':
                pygame.draw.circle(window, line_color,
                                   (col * cell_width + cell_width // 2, row * cell_height + cell_height // 2),
                                   cell_width // 2, 2)

def player_turn():
    turn_text = font.render('Player: X' if game_over or turn == 'O' else 'Player: O', True, line_color, line_color1)
    window.blit(turn_text, (100, cell_height * 4))

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

    # Gamepad-Steuerung
    for joystick in joysticks:
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)

            # Pfeiltasten für die Auswahl bewegen
            if i == 0 and axis_value < -0.5:
                selected_col = (selected_col - 1) % 3
            elif i == 0 and axis_value > 0.5:
                selected_col = (selected_col + 1) % 3
            elif i == 1 and axis_value < -0.5:
                selected_row = (selected_row - 1) % 3
            elif i == 1 and axis_value > 0.5:
                selected_row = (selected_row + 1) % 3

        for i in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(i)

            # Bestätigungstaste (z.B., Button 1)
            if i == 1 and button_state == 1:
                if game_board[selected_row][selected_col] == '':
                    game_board[selected_row][selected_col] = turn
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
        winner_text = font.render('Winner: ' + winner, True, line_color, line_color1)
        window.blit(winner_text, (100, cell_height * 4))
    elif all(game_board[i][j] != '' for i in range(3) for j in range(3)):
        game_over = True
        draw_text = font.render('   DRAW   ', True, line_color, line_color1)
        window.blit(draw_text, (100, cell_height * 4))

    # Markiere die ausgewählte Zelle
    pygame.draw.rect(window, line_color, (selected_col * cell_width, selected_row * cell_height, cell_width, cell_height), 2)

    pygame.display.flip()

pygame.quit()
sys.exit()
