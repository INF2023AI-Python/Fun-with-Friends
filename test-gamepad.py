import pygame
import sys

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect a joystick and try again.")
    sys.exit()
else:
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print(f"Joystick {i + 1} detected. ID: {joystick.get_id()}")

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

    clock.tick(60)

pygame.quit()
sys.exit()
