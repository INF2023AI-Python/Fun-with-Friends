import time
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import sys

# Starting position of the orange square
orange_square_position = [1, 1]

# Player 1 starts with 'X'
current_player = 'X'

# Function to draw the Tic Tac Toe board on the RGB LED matrix
def draw_board(board_state, offset_canvas, matrix):
    for row in range(32):
        for col in range(32):
            # Draw the grid
            if row % 10 == 0 or col % 10 == 0:
                offset_canvas.SetPixel(col, row, 100, 100, 100)

    # Draw the game symbols
    for row in range(3):
        for col in range(3):
            if board_state[row][col] == 'O':
                graphics.DrawCircle(offset_canvas, col * 10 + 5, row * 10 + 5, 4, graphics.Color(0, 0, 255))
            elif board_state[row][col] == 'X':
                x1, y1, x2, y2 = col * 10 + 1, row * 10 + 1, col * 10 + 9, row * 10 + 9
                graphics.DrawLine(offset_canvas, x1, y1, x2, y2, graphics.Color(255, 0, 0))
                graphics.DrawLine(offset_canvas, x2, y1, x1, y2, graphics.Color(255, 0, 0))

    # Draw the orange square
    x1, y1, x2, y2 = orange_square_position[0] * 10, orange_square_position[1] * 10, (orange_square_position[0] + 1) * 10, (orange_square_position[1] + 1) * 10
    graphics.DrawLine(offset_canvas, x1, y1, x2, y1, graphics.Color(255, 165, 0))
    graphics.DrawLine(offset_canvas, x2, y1, x2, y2, graphics.Color(255, 165, 0))
    graphics.DrawLine(offset_canvas, x2, y2, x1, y2, graphics.Color(255, 165, 0))
    graphics.DrawLine(offset_canvas, x1, y2, x1, y1, graphics.Color(255, 165, 0))
    
    return matrix.SwapOnVSync(offset_canvas)

# Function to check the game status (win, draw)
def check_winner(board_state):
    for row in range(3):
        if board_state[row][0] == board_state[row][1] == board_state[row][2] != ' ':
            return True

    for col in range(3):
        if board_state[0][col] == board_state[1][col] == board_state[2][col] != ' ':
            return True

    if board_state[0][0] == board_state[1][1] == board_state[2][2] != ' ':
        return True

    if board_state[0][2] == board_state[1][1] == board_state[2][0] != ' ':
        return True

    return False

# Function to update the Tic Tac Toe board based on joystick inputs
def update_board_with_joystick(board_state, joystick, offset_canvas, matrix):
    global orange_square_position
    global current_player

    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Movement direction based on axis values with tolerance
    if -0.2 < x_axis < 0.2 and y_axis < -0.8:
        # Move up
        orange_square_position[1] = max(0, orange_square_position[1] - 1)
    elif -0.2 < x_axis < 0.2 and y_axis > 0.8:
        # Move down
        orange_square_position[1] = min(2, orange_square_position[1] + 1)
    elif x_axis > 0.8 and -0.2 < y_axis < 0.2:
        # Move right
        orange_square_position[0] = min(2, orange_square_position[0] + 1)
    elif x_axis < -0.8 and -0.2 < y_axis < 0.2:
        # Move left
        orange_square_position[0] = max(0, orange_square_position[0] - 1)

    if joystick.get_button(1) == 1:
        set_x_or_o(board_state, offset_canvas, matrix)
    elif joystick.get_button(9) == 1:
        pygame.quit()

# Function to set 'X' or 'O' on the Tic Tac Toe board
def set_x_or_o(board_state, offset_canvas, matrix):
    global orange_square_position
    global current_player

    # Check if the selected cell is empty (' ')
    if board_state[orange_square_position[1]][orange_square_position[0]] == ' ':
        board_state[orange_square_position[1]][orange_square_position[0]] = current_player
        if check_winner(board_state):
            print(f"Player {current_player} wins!")
            draw_board(board_state, offset_canvas, matrix)  # Update one last time before ending to display the winner
            time.sleep(0.5)
            matrix.Clear()
            display_winner(current_player, offset_canvas, matrix)  # Display win message on the LED matrix
            matrix.Clear()
            return
        current_player = 'X' if current_player == 'O' else 'O'  # Switch the current player
        print(f"Player {current_player}")

# Function to create a canvas and display the text
def display_text(text, color, offset_canvas, matrix):
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
    textColor = graphics.Color(*color)

    # Display the text of the first line
    graphics.DrawText(offset_canvas, font, 2, 10, textColor, text[0])
    # Display the text of the second line
    graphics.DrawText(offset_canvas, font, 2, 20, textColor, text[1])
    # Display the text of the third line
    graphics.DrawText(offset_canvas, font, 2, 30, textColor, text[2])

    return matrix.SwapOnVSync(offset_canvas)

# Display win screen
def display_winner(player, offset_canvas, matrix):
    color = (255, 0, 0) if player == 'X' else (0, 0, 255)  # Red for player X, Blue for player O
    offset_canvas = display_text(["WIN", "Player", player], color, offset_canvas, matrix)
    time.sleep(5)
    return offset_canvas

# Display draw screen
def display_draw(offset_canvas, matrix):
    time.sleep(0.5)
    matrix.Clear()
    color = (255, 255, 255)  # White for draw
    offset_canvas = display_text(["", "DRAW", ""], color, offset_canvas, matrix)
    time.sleep(5)
    matrix.Clear()
    return offset_canvas

# Main game loop function
def tictactoe(offset_canvas, matrix):
    # Initialize the Tic Tac Toe board
    board_state = [[' ' for _ in range(3)] for _ in range(3)]

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected. Please connect a joystick and try again.")
        pygame.quit()
        sys.exit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        offset_canvas = draw_board(board_state, offset_canvas, matrix)
        update_board_with_joystick(board_state, joystick, offset_canvas, matrix)

        if check_winner(board_state):
            return
        elif ' ' not in [cell for row in board_state for cell in row]:
            draw_board(board_state, offset_canvas, matrix)  # Update one last time before ending to display the draw
            offset_canvas = display_draw(offset_canvas, matrix)  # Display draw message on the LED matrix
            return

        pygame.time.Clock().tick(10)  # Add a delay to make the board more visible