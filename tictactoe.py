import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import pygame
import sys
import os

os.environ['PULSE_SERVER'] = '127.0.0.1:6666'

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

    # Zeichne ein Quadrat auf der Matrix
    graphics.DrawLine(matrix, 5, 5, 15, 5, graphics.Color(255, 255, 255))
    graphics.DrawLine(matrix, 15, 5, 15, 15, graphics.Color(255, 255, 255))
    graphics.DrawLine(matrix, 15, 15, 5, 15, graphics.Color(255, 255, 255))
    graphics.DrawLine(matrix, 5, 15, 5, 5, graphics.Color(255, 255, 255))

    # Aktualisiere die Matrix
    matrix.SwapOnVSync()

    clock.tick(60)

pygame.mixer.quit()
pygame.quit()
sys.exit()
