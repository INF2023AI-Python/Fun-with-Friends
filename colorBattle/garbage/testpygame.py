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

#??????????????????
joysticks[0].init()
joysticks[1].init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)



# Player variables
player_size = 1
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
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * player1_speed)
            player1_y += int(axis_y * player1_speed)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)

    # Wrap player 1 around the screen borders
    if player1_x < 0:
        player1_x = width - player_size
    elif player1_x >= width:
        player1_x = 0
    if player1_y < 0:
        player1_y = height - player_size
    elif player1_y >= height:
        player1_y = 0

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


    # Convert Pygame surface to RGBMatrix format
    pygame.surfarray.blit_array(matrix, pygame.surfarray.array3d(screen))

    # Refresh display
    matrix.UpdateScreen()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()