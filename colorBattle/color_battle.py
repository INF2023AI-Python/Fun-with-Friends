import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Color Battle 1.0")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Player variables
player_size = 10
player1_x = width // 4   #
player1_y = height // 2
player1_speed = 10
player1_color = (255, 0, 0)  # Red
player1_trail_color = (0, 255, 0)  # Green trail for Player 1 (weaker)

player2_x = 3 * width // 4 # start position
player2_y = height // 2
player2_speed = 10
player2_color = (0, 0, 255)  # Blue
player2_trail_color = (255, 255, 0)  # Yellow trail for Player 2 (stronger)

# trails = [[]]
game_area = [[0 for _ in range(width)] for _ in range(height)]

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle keyboard input
    keys = pygame.key.get_pressed()

    # TODO: change the controls for gamepad
    # Player 1 controls (WASD)
    if keys[pygame.K_w]:
        player1_y -= player1_speed
    if keys[pygame.K_s]:
        player1_y += player1_speed
    if keys[pygame.K_a]:
        player1_x -= player1_speed
    if keys[pygame.K_d]:
        player1_x += player1_speed

    # Wrap player 1 around the screen borders
    if player1_x < 0:
        player1_x = width - player_size
    elif player1_x >= width:
        player1_x = 0
    if player1_y < 0:
        player1_y = height - player_size
    elif player1_y >= height:
        player1_y = 0

    # Player 2 controls (Arrow keys)
    if keys[pygame.K_UP]:
        player2_y -= player2_speed
    if keys[pygame.K_DOWN]:
        player2_y += player2_speed
    if keys[pygame.K_LEFT]:
        player2_x -= player2_speed
    if keys[pygame.K_RIGHT]:
        player2_x += player2_speed

    # Wrap player 2 around the screen borders
    if player2_x < 0:
        player2_x = width - player_size
    elif player2_x >= width:
        player2_x = 0
    if player2_y < 0:
        player2_y = height - player_size
    elif player2_y >= height:
        player2_y = 0

    # Check for painting over and handle wrapping around the screen
    game_area[int(player1_y)][int(player1_x)] = 1  # Player 1
    game_area[int(player2_y)][int(player2_x)] = 2  # Player 2

    # Draw
    screen.fill(black)

    # Draw trails

    for y in range(height):
        for x in range(width):
            if game_area[y][x] == 1:
                pygame.draw.rect(screen, player1_trail_color, (x, y, player_size, player_size))
            elif game_area[y][x] == 2:
                pygame.draw.rect(screen, player2_trail_color, (x, y, player_size, player_size))

    # Draw players
    pygame.draw.rect(screen, player1_color, (player1_x, player1_y, player_size, player_size))
    pygame.draw.rect(screen, player2_color, (player2_x, player2_y, player_size, player_size))

    # Refresh display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

