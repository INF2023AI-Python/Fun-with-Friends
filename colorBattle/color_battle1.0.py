import random
import pygame
from time import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


# def generate_bonus_points(game_area, bonus_points):
#     for _ in range(bonus_points):
#         x = random.randint(0, len(game_area[0]) - 1)
#         y = random.randint(0, len(game_area) - 1)
#         # Ensure bonus points don't overlap with player positions
#         while game_area[y][x] != 0:
#             x = random.randint(0, len(game_area[0]) - 1)
#             y = random.randint(0, len(game_area) - 1)
#         game_area[y][x] = 'B'  # Mark bonus points on the game area


# def draw_bonus_points(canvas, game_area, player_size, blink_state, offset_x, offset_y):
#     for y in range(len(game_area)):
#         for x in range(len(game_area[0])):
#             if game_area[y][x] == 'B':
#                 if blink_state:
#                     canvas.SetPixel((x + offset_x) * player_size, (y + offset_y) * player_size, 255, 255, 255)
#                 else:
#                     canvas.SetPixel((x + offset_x) * player_size, (y + offset_y) * player_size, 0, 0, 0)
#

def count_points(game_area):
    player1_count = sum(row.count(1) for row in game_area)  # Count cells occupied by player 1
    player2_count = sum(row.count(2) for row in game_area)  # Count cells occupied by player 2

    return player1_count, player2_count


def color_battle():
    # Initialize Pygame
    pygame.init()

    # Set up gamepads
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

    # Set up display
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Color Battle 1.0")

    # Define colors
    # white = (255, 255, 255)
    black = (0, 0, 0)

    # Player variables
    player_size = 10
    player1_x = width // 4  #
    player1_y = height // 2
    player1_speed = 10
    player1_color = (255, 0, 0)  # Red
    player1_trail_color = (0, 255, 0)  # Green trail for Player 1 (weaker)

    player2_x = 3 * width // 4  # start position
    player2_y = height // 2
    player2_speed = 10
    player2_color = (0, 0, 255)  # Blue
    player2_trail_color = (255, 255, 0)  # Yellow trail for Player 2 (stronger)

    # trails = [[]]
    game_area = [[0 for _ in range(width)] for _ in range(height)]

    # Game duration
    game_duration = 60  # 60 seconds

    # Start time
    start_time = time()

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle keyboard input
        keys = pygame.key.get_pressed()

        # gamepads axis control player movement
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

        # Check if game duration has elapsed
        if time() - start_time >= game_duration:
            running = False

        # Refresh display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Determine the winner based on the counts
    player1_count, player2_count = count_points(game_area)

    if player1_count == player2_count:
        print("It's a tie!")
    elif player1_count > player2_count:
        print("Green PLayer wins!")
    else:
        print("Yellow Player wins!")
    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    color_battle()
