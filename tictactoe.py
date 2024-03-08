import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import sys

# Konfiguration der LED-Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"

matrix = RGBMatrix(options=options)

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    sys.exit()
else:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"Joystick {i} detected. ID: {joystick.get_id()}")

joystick = pygame.joystick.Joystick(0)
joystick.init()

running = True
clock = pygame.time.Clock()

# Speichere die vorherigen Zustände von Achsen und Tasten
prev_axes_states = [[0.0] * joystick.get_numaxes() for joystick in joysticks]
prev_buttons_states = [[0] * joystick.get_numbuttons() for joystick in joysticks]

# Tic-Tac-Toe-Feld erstellen
field = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

def draw_tic_tac_toe(matrix, field):
    matrix.Clear()

    # Zeichne das Tic-Tac-Toe-Feld
    for row in range(1, 3):
        graphics.DrawLine(matrix, 0, row * 10, matrix.width, row * 10, graphics.Color(255, 255, 255))

    for col in range(1, 3):
        graphics.DrawLine(matrix, col * 10, 0, col * 10, matrix.height, graphics.Color(255, 255, 255))

    # Zeichne X und O basierend auf dem Spielfeld
    for row in range(3):
        for col in range(3):
            if field[row][col] == 1:
                graphics.DrawLine(matrix, col * 10, row * 10, (col + 1) * 10, (row + 1) * 10, graphics.Color(255, 0, 0))
                graphics.DrawLine(matrix, col * 10, (row + 1) * 10, (col + 1) * 10, row * 10, graphics.Color(255, 0, 0))
            elif field[row][col] == 2:
                graphics.DrawCircle(matrix, col * 10 + 5, row * 10 + 5, 5, graphics.Color(0, 0, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.JOYAXISMOTION:
            axis_id = event.axis
            axis_position = event.value
            print(f"Joystick {event.joy}, Axis {axis_id}: {axis_position:.2f}")
        elif event.type == pygame.JOYBUTTONDOWN:
            button_id = event.button
            print(f"Joystick {event.joy}, Button {button_id}: {button_state}")

    # Aktualisiere die vorherigen Zustände für Achsen und Buttons
    for i, joystick in enumerate(joysticks):
        for axis_id in range(joystick.get_numaxes()):
            axis_position = joystick.get_axis(axis_id)
            if axis_position != prev_axes_states[i][axis_id]:
                print(f"Joystick {i}, Axis {axis_id}: {axis_position:.2f}")
                prev_axes_states[i][axis_id] = axis_position

        for button_id in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(button_id)
            if button_state != prev_buttons_states[i][button_id]:
                print(f"Joystick {i}, Button {button_id}: {button_state}")
                prev_buttons_states[i][button_id] = button_state

    # Zeichne das Tic-Tac-Toe-Feld auf der Matrix
    draw_tic_tac_toe(matrix, field)
    time.sleep(0.1)

pygame.mixer.quit()
pygame.quit()
sys.exit()
