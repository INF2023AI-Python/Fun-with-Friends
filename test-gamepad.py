import pygame
import sys

pygame.init()

# Initialisiere die Joysticks außerhalb der Schleife
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Terminalausgabe der Achsenpositionen und Button-Zustände
    for i, joystick in enumerate(joysticks):
        for axis_id in range(joystick.get_numaxes()):
            axis_position = joystick.get_axis(axis_id)
            print(f"Joystick {i}, Axis {axis_id}: {axis_position:.2f}")

        for button_id in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(button_id)
            print(f"Joystick {i}, Button {button_id}: {button_state}")

    clock.tick(60)

pygame.quit()
sys.exit()
