import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

width, height = 32, 32  # Set according to your RGB matrix dimensions
screen = pygame.display.set_mode((width, height))

# Configuration for Matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options=options)

# Initialize Pygame
pygame.init()

# Set up gamepads
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

if not joysticks:
    print("No gamepads detected. Exiting.")
    pygame.quit()
    sys.exit()

joysticks[0].init()
joysticks[1].init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Player variables
player_size = 1
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

    # Update player positions based on gamepad input
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * player1_speed)
            player1_y += int(axis_y * player1_speed)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)


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


# Convert Pygame surface to RGBMatrix format
    pygame.surfarray.blit_array(matrix, pygame.surfarray.array3d(screen))

    # Refresh display
    matrix.UpdateScreen()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()