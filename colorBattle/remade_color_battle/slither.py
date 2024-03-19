import pygame
import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32
BLOCK_SIZE = 1
APPLE_THICKNESS = 1
FPS = 30

# Initialize the RGBMatrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
gameDisplay = matrix.CreateFrameCanvas()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define apple color
apple_color = RED  # You can change this to any color you like


clock = pygame.time.Clock()

# Directions for each player
direction_p1 = "right"
direction_p2 = "left"

# Function to display score on RGBMatrix
def score(score):
    pass  # Placeholder for displaying score on RGBMatrix

# Function to generate a random apple position
def rand_apple_gen():
    rand_apple_x = random.randrange(0, SCREEN_WIDTH - APPLE_THICKNESS)
    rand_apple_y = random.randrange(0, SCREEN_HEIGHT - APPLE_THICKNESS)
    return rand_apple_x, rand_apple_y

rand_apple_x, rand_apple_y = rand_apple_gen()

# Main game loop
# Main game loop
def game_loop():
    global direction_p1, direction_p2
    game_exit = False
    game_over = False

    # Will be the leader of the #1 block of the snake
    lead_x_p1 = SCREEN_WIDTH / 4
    lead_y_p1 = SCREEN_HEIGHT / 2
    lead_x_change_p1 = BLOCK_SIZE
    lead_y_change_p1 = 0

    lead_x_p2 = (SCREEN_WIDTH / 4) * 3
    lead_y_p2 = SCREEN_HEIGHT / 2
    lead_x_change_p2 = -BLOCK_SIZE
    lead_y_change_p2 = 0

    # list is for the length of the snake (Note: the last item in list is the head)
    snake_list_p1 = []
    snake_list_p2 = []
    snake_length_p1 = 1
    snake_length_p2 = 1

    rand_apple_x, rand_apple_y = rand_apple_gen()

    # Main game loop
    while not game_exit:
        if game_over:
            # Handle game over logic here
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_exit = True

        # Read gamepad inputs
        for joystick in joysticks:
            if joystick.get_name() == "YourFirstGamepadName":
                # Handle gamepad inputs for player 1
                if joystick.get_button(0):
                    direction_p1 = "left"
                    lead_x_change_p1 = -BLOCK_SIZE
                    lead_y_change_p1 = 0
                elif joystick.get_button(1):
                    direction_p1 = "right"
                    lead_x_change_p1 = BLOCK_SIZE
                    lead_y_change_p1 = 0
                elif joystick.get_button(2):
                    direction_p1 = "up"
                    lead_y_change_p1 = -BLOCK_SIZE
                    lead_x_change_p1 = 0
                elif joystick.get_button(3):
                    direction_p1 = "down"
                    lead_y_change_p1 = BLOCK_SIZE
                    lead_x_change_p1 = 0

            elif joystick.get_name() == "YourSecondGamepadName":
                # Handle gamepad inputs for player 2
                if joystick.get_button(0):
                    direction_p2 = "left"
                    lead_x_change_p2 = -BLOCK_SIZE
                    lead_y_change_p2 = 0
                elif joystick.get_button(1):
                    direction_p2 = "right"
                    lead_x_change_p2 = BLOCK_SIZE
                    lead_y_change_p2 = 0
                elif joystick.get_button(2):
                    direction_p2 = "up"
                    lead_y_change_p2 = -BLOCK_SIZE
                    lead_x_change_p2 = 0
                elif joystick.get_button(3):
                    direction_p2 = "down"
                    lead_y_change_p2 = BLOCK_SIZE
                    lead_x_change_p2 = 0

        # Handle snake movement and collision detection for player 1
        lead_x_p1 += lead_x_change_p1
        lead_y_p1 += lead_y_change_p1
        # Update snake position, check for collisions, etc. for player 1

        # Handle snake movement and collision detection for player 2
        lead_x_p2 += lead_x_change_p2
        lead_y_p2 += lead_y_change_p2

        # Creates the boundaries for the game
        if lead_x >= SCREEN_WIDTH or lead_x < 0 or lead_y >= SCREEN_HEIGHT or lead_y < 0:
            game_over = True

        # Adds or subtracts from lead_x
        lead_x += lead_x_change_p1
        lead_y += lead_y_change_p1

      # Draw a rectangle representing the apple
        for x in range(rand_apple_x, rand_apple_x + APPLE_THICKNESS):
            for y in range(rand_apple_y, rand_apple_y + APPLE_THICKNESS):
                gameDisplay.SetPixel(x, y, *apple_color)



        # creates the snake and will make it longer by appending last known place
        snake_head_p1 = []
        snake_head_p1.append(lead_x)
        snake_head_p1.append(lead_y)
        snake_list_p1.append(snake_head_p1)

        if len(snake_list_p1) > snake_length_p1:
            del snake_list_p1[0]

        for each_segment in snake_list_p1[:-1]:
            if each_segment == snake_head_p1:
                game_over = True

        # Draw player 1's snake
        for XnY in snake_list_p1:
            gameDisplay.SetPixel(XnY[0], XnY[1], *GREEN)

        # Draw player 2's snake
        for XnY in snake_list_p2:
            gameDisplay.SetPixel(XnY[0], XnY[1], *WHITE)


        # Update the display
        matrix.SwapOnVSync(gameDisplay)

        # Specify FPS
        clock.tick(FPS)

    # Uninitialize the module
    pygame.quit()
    quit()

game_loop()
