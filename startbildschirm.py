import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import subprocess
from tictactoe.tictactoe import tictactoe
from VierGewinnt.VierGewinnt import vierGewinnt
from snake.snake import snake

orange_square_position = [0, 0]

# Matrix configuration
options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Function to clear the screen
def clear_screen():
    global matrix
    matrix.Clear()

# Function to draw the screen (grid, icons, selection)
def draw_screen(x, y, offset_canvas, matrix):
    color = (255, 255, 255) # white
    red = (255, 0, 0)
    blue = (0, 0, 255)
    orange = (255, 165, 0)

    # Vertical lines
    for row in range(32):
        offset_canvas.SetPixel(0, row, *color)
        offset_canvas.SetPixel(15, row, *color)
        offset_canvas.SetPixel(31, row, *color)

    # Horizontal lines
    for col in range(32):
        offset_canvas.SetPixel(col, 0, *color)
        offset_canvas.SetPixel(col, 15, *color)
        offset_canvas.SetPixel(col, 31, *color)

    # Position of the orange square scaled to 0-15
    x_pos = int(x * 15)
    y_pos = int(y * 15)

    # Orange square
    # Top line
    if x_pos % 16 == 0 and y_pos % 16 != 0:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, y_pos, *orange)
    elif x_pos % 16 != 0 and y_pos % 16 == 0:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, y_pos, *orange)
    elif x_pos % 16 != 0 and y_pos % 16 != 0:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, y_pos, *orange)
            offset_canvas.SetPixel(x_pos, i + y_pos, *orange)
    else:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, y_pos, *orange)
            offset_canvas.SetPixel(x_pos, i + y_pos, *orange)

    # Bottom line
    if y_pos == 15 and x_pos == 15:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, 16 + y_pos, *orange)
            offset_canvas.SetPixel(31, 31, *orange)
    elif y_pos == 0 and x_pos == 0:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, 15 + y_pos, *orange)
    elif y_pos == 0 and x_pos == 15:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, 15 + y_pos, *orange)
    elif y_pos == 15 and x_pos == 0:
        for i in range(16):
            offset_canvas.SetPixel(i + x_pos, 16 + y_pos, *orange)
    # Left line
    for i in range(16):
        offset_canvas.SetPixel(x_pos, i + y_pos, *orange)
    # Right line
    if x_pos == 15:
        for i in range(16):
            offset_canvas.SetPixel(16 + x_pos, i + y_pos, *orange)
    elif x_pos == 0:
        for i in range(16):
            offset_canvas.SetPixel(15 + x_pos, i + y_pos, *orange)

    # Draw icons
    # Colorbattle
    for row in range(2, 7):
        for col in range(5, 10):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(9, 14):
        for col in range(5, 10):
            offset_canvas.SetPixel(row, col, *blue)

    # Tictactoe
    positionsX = [
        (17, 4), (18, 5), (19, 6), (20, 7), (21, 6), (22, 5), (23, 4),
        (19, 8), (21, 8), (18, 9), (22, 9), (17, 10), (23, 10)
    ]
    for pos in positionsX:
        offset_canvas.SetPixel(pos[0], pos[1], *red)
    positionsO = [
        (24, 6), (24, 7), (24, 8), (25, 5), (25, 9), (26, 4), (26, 10),
        (27, 4), (27, 10), (28, 5), (28, 9), (29, 6), (29, 7), (29, 8)
    ]
    for pos in positionsO:
        offset_canvas.SetPixel(pos[0], pos[1], *blue)

    # Connect Four
    for row in range(2, 5):
        for col in range(27, 30):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(5, 8):
        for col in range(24, 30):
            offset_canvas.SetPixel(row, col, *blue)
    for row in range(8, 11):
        for col in range(21, 30):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(18, 24):
            offset_canvas.SetPixel(row, col, *blue)
    for row in range(11, 14):
        for col in range(24, 27):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(27, 30):
            offset_canvas.SetPixel(row, col, *blue)

    # ShutDown
    for row in range(22, 24):
        for col in range(17, 23):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(21, 25):
        for col in range(27, 29):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(19, 21):
        for col in range(25, 27):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(25, 27):
        for col in range(25, 27):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(17, 19):
        for col in range(21, 25):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(27, 29):
        for col in range(21, 25):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(19, 21):
        for col in range(19, 21):
            offset_canvas.SetPixel(row, col, *red)
    for row in range(25, 27):
        for col in range(19, 21):
            offset_canvas.SetPixel(row, col, *red)
    return matrix.SwapOnVSync(offset_canvas)

def select_option(new_position):
    global offset_canvas
    global matrix
    if new_position[0] == 0 and new_position[1] == 0:
        clear_screen()
        snake(offset_canvas, matrix)
        print("Snake selected")
        
    elif new_position[0] == 1 and new_position[1] == 0:
        clear_screen()
        tictactoe(offset_canvas, matrix)
        print("Tictactoe selected")
        
    elif new_position[0] == 0 and new_position[1] == 1:
        vierGewinnt(offset_canvas, matrix)
        print("Connect Four selected")
        
    elif new_position[0] == 1 and new_position[1] == 1:
        print("ShutDown selected")
        subprocess.call("sudo shutdown -h now", shell=True)


def update_orange_square_position(orange_square_position, joystick):
   
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Movement direction based on axis values with tolerance
    if -0.2 < x_axis < 0.2 and y_axis < -0.8:
        # Move up
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] - 1))]
        print("Move up")
    elif -0.2 < x_axis < 0.2 and y_axis > 0.8:
        # Move down
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] + 1))]
        print("Move down")
    elif x_axis > 0.8 and -0.2 < y_axis < 0.2:
        # Move right
        new_position = [max(0, min(1, orange_square_position[0] + 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Move right")
    elif x_axis < -0.8 and -0.2 < y_axis < 0.2:
        # Move left
        new_position = [max(0, min(1, orange_square_position[0] - 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Move left")
    else:
        new_position = orange_square_position

    if joystick.get_button(1) == 1:
        select_option(new_position)

    return new_position



def main():
    global orange_square_position
    global matrix
    global offset_canvas

    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick found.")
        pygame.quit()
        quit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    running = True
    while running:
        orange_square_position = update_orange_square_position(orange_square_position, joystick)
        draw_screen(orange_square_position[0], orange_square_position[1], offset_canvas, matrix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()