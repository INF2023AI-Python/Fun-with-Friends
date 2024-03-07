import os
import pygame
from time import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import random

# Constants and Configurations
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
PLAYER_SIZE = 1
GAME_DURATION = 60
PLAYER_SPEED = 1

def initialize_game():
    global player1_x, player1_y, player2_x, player2_y
    player1_x = SCREEN_WIDTH // 4
    player1_y = SCREEN_HEIGHT // 2

    player2_x = 3 * SCREEN_WIDTH // 4
    player2_y = SCREEN_HEIGHT // 2

    # Additional initialization code...

def update_game_state():
    global player1_x, player1_y, player2_x, player2_y, game_area
    # Handle player movement, wrapping, and other game state updates...

    # Example: Player 1 wraps around the screen borders
    if player1_x < 0:
        player1_x = SCREEN_WIDTH - PLAYER_SIZE
    elif player1_x >= SCREEN_WIDTH:
        player1_x = 0
    if player1_y < 0:
        player1_y = SCREEN_HEIGHT - PLAYER_SIZE
    elif player1_y >= SCREEN_HEIGHT:
        player1_y = 0

    # Example: Player 2 wraps around the screen borders
    if player2_x < 0:
        player2_x = SCREEN_WIDTH - PLAYER_SIZE
    elif player2_x >= SCREEN_WIDTH:
        player2_x = 0
    if player2_y < 0:
        player2_y = SCREEN_HEIGHT - PLAYER_SIZE
    elif player2_y >= SCREEN_HEIGHT:
        player2_y = 0

    # Additional game state updates...

def determine_winner(player1, player2):
    player1_count = sum(row.count(1) for row in game_area)
    player2_count = sum(row.count(2) for row in game_area)

    if player1_count == player2_count:
        print("It's a tie!")
    elif player1_count > player2_count:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")

def generate_bonus_points(game_area, bonus_points):
    for _ in range(bonus_points):
        x = random.randint(0, len(game_area[0]) - 1)
        y = random.randint(0, len(game_area) - 1)
        # Ensure bonus points don't overlap with player positions
        while game_area[y][x] != 0:
            x = random.randint(0, len(game_area[0]) - 1)
            y = random.randint(0, len(game_area) - 1)
        game_area[y][x] = 'B'  # Mark bonus points on the game area

def draw_bonus_points(matrix, game_area, player_size, blink_state):
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if game_area[y][x] == 'B':
                if blink_state:
                    matrix.SetPixel(x, y, 255, 255, 255)
                else:
                    matrix.SetPixel(x, y, 0, 0, 0)

def draw_game_screen(matrix, game_area, player_size, player1_color, player2_color, player1_trail_color, player2_trail_color):
    # Draw trails on the matrix
    matrix.Clear()
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            if game_area[y][x] == 1:
                matrix.SetPixel(x, y, *player1_trail_color)
            elif game_area[y][x] == 2:
                matrix.SetPixel(x, y, *player2_trail_color)

    # Draw players on the matrix
    matrix.SetPixel(player1_x, player1_y, *player1_color)
    matrix.SetPixel(player2_x, player2_y, *player2_color)

def handle_player_movement(keys, joysticks):
    global player1_x, player1_y, player2_x, player2_y, PLAYER_SPEED

    # Handle keyboard input
    if keys[pygame.K_LEFT]:
        player1_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player1_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player1_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player1_y += PLAYER_SPEED

    # Gamepads axis control player movement
    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * PLAYER_SPEED)
            player1_y += int(axis_y * PLAYER_SPEED)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * PLAYER_SPEED)
            player2_y += int(axis_y * PLAYER_SPEED)

    # Additional handling if needed...

    # Ensure players stay within the screen boundaries
    player1_x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, player1_x))
    player1_y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, player1_y))

    player2_x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, player2_x))
    player2_y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, player2_y))

def draw_bonus_points(canvas, game_area, player_size, blink_state, offset_x, offset_y):
    for y in range(len(game_area)):
        for x in range(len(game_area[0])):
            if game_area[y][x] == 'B':
                if blink_state:
                    canvas.SetPixel((x + offset_x) * player_size, (y + offset_y) * player_size, 255, 255, 255)
                else:
                    canvas.SetPixel((x + offset_x) * player_size, (y + offset_y) * player_size, 0, 0, 0)

def determine_winner(game_area):
    player1_count = sum(row.count(1) for row in game_area)
    player2_count = sum(row.count(2) for row in game_area)

    if player1_count == player2_count:
        print("It's a tie!")
    elif player1_count > player2_count:
        print("Player 1 wins!")
    else:
        print("Player 2 wins!")

def main():
    global player1_x, player1_y, player2_x, player2_y, game_area
    blink_state = True
    # Initialization code...
    initialize_game()

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    options.drop_privileges = 0  # DONT DROP PRIVS!!!

    # Setup screen
    screen = pygame.display.set_mode((SCREEN_WIDTH*2, SCREEN_HEIGHT))
    pygame.display.set_caption("Color Battle 1.0")

    # Setup different screen halves
    changing_screen = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    changing_matrix_screen = (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Matrix & Canvas
    matrix = RGBMatrix(options=options)
    offset_canvas = matrix.CreateFrameCanvas()

    # Initialize Pygame
    pygame.init()

    # Set up gamepads
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Player variables
    player1_x = SCREEN_WIDTH // 4
    player1_y = SCREEN_HEIGHT // 2
    player1_color = (255, 0, 0)  # Red
    player1_trail_color = (0, 255, 0)  # Green trail for Player 1 (weaker)

    player2_x = 3 * SCREEN_WIDTH // 4
    player2_y = SCREEN_HEIGHT // 2
    player2_color = (0, 0, 255)  # Blue
    player2_trail_color = (255, 255, 0)  # Yellow trail for Player 2 (stronger)

    game_area = [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    # Game duration
    game_duration = GAME_DURATION  # 60 seconds

    # Start time
    start_time = time()

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_player_movement(pygame.key.get_pressed(), joysticks)

        update_game_state()

        draw_game_screen(offset_canvas, game_area, PLAYER_SIZE, player1_color, player2_color, player1_trail_color, player2_trail_color)
        draw_bonus_points(offset_canvas, game_area, PLAYER_SIZE, blink_state)  # Add this line

        offset_canvas = matrix.SwapOnVSync(offset_canvas)

        # Check if game duration has elapsed
        if time() - start_time >= game_duration:
            running = False

        # Cap the frame rate
        clock.tick(60)

        determine_winner(game_area)

    pygame.quit()

if __name__ == "__main__":
    main()
