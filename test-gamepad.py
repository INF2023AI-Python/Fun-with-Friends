import pygame
import sys

pygame.init()

window_width = 400
window_height = 300
window = pygame.display.set_mode((window_width, window_height))
font = pygame.font.Font(None, 36)  # Schriftart und Größe

# Initialisiere die Joysticks außerhalb der Schleife
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    window.fill((255, 255, 255))  # Hintergrundfarbe des Fensters

    # Anzeige der Achsenpositionen und Button-Zustände im Fenster
    for i, joystick in enumerate(joysticks):
        for axis_id in range(joystick.get_numaxes()):
            axis_position = joystick.get_axis(axis_id)
            text_axis = font.render(f"Joystick {i}, Axis {axis_id}: {axis_position:.2f}", True, (0, 0, 0))
            window.blit(text_axis, (10, 10 + 30 * (axis_id + i * joystick.get_numaxes())))

        for button_id in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(button_id)
            text_button = font.render(f"Joystick {i}, Button {button_id}: {button_state}", True, (0, 0, 0))
            window.blit(text_button, (10, 150 + 30 * (button_id + i * joystick.get_numbuttons())))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
