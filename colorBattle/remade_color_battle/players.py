import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640


def players_init():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    players_size = 10

    player1_x = SCREEN_WIDTH // 4
    player1_y = SCREEN_HEIGHT // 4

    player1_speed = 10
    player1_color = (255, 0, 0)
    player1_trail_color = (0, 255, 0)

    player2_x = 3 * SCREEN_WIDTH // 4  # start position
    player2_y = SCREEN_HEIGHT // 2
    player2_speed = 10
    player2_color = (0, 0, 255)  # Blue
    player2_trail_color = (255, 255, 0)  # Yellow trail for Player 2

