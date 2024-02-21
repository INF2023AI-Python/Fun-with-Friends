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
player1_x = width // 4
player1_y = height // 2
player1_speed = 5
player1_color = (255, 0, 0)  # Red

player2_x = 3 * width // 4
player2_y = height // 2
player2_speed = 5
player2_color = (0, 0, 255)  # Blue

# Trail variables
trail1 = []
trail2 = []

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle keyboard input
    keys = pygame.key.get_pressed()

    # Player 1 controls (WASD)
    if keys[pygame.K_w]:
        player1_y -= player1_speed
    if keys[pygame.K_s]:
        player1_y += player1_speed
    if keys[pygame.K_a]:
        player1_x -= player1_speed
    if keys[pygame.K_d]:
        player1_x += player1_speed

    # Player 2 controls (Arrow keys)
    if keys[pygame.K_UP]:
        player2_y -= player2_speed
    if keys[pygame.K_DOWN]:
        player2_y += player2_speed
    if keys[pygame.K_LEFT]:
        player2_x -= player2_speed
    if keys[pygame.K_RIGHT]:
        player2_x += player2_speed

    # Append current position to trail
    trail1.append((player1_x, player1_y))
    trail2.append((player2_x, player2_y))

    # Draw
    screen.fill(black)

    # Draw trails
    for point in trail1:
        pygame.draw.rect(screen, player1_color, (point[0], point[1], player_size, player_size))
    for point in trail2:
        pygame.draw.rect(screen, player2_color, (point[0], point[1], player_size, player_size))

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
