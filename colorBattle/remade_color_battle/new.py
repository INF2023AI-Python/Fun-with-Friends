import pygame
import random
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640  # Window size
ROWS, COLS = 32, 32  # Grid size
CELL_SIZE = WIDTH // COLS
GAME_DURATION = 60  # Game duration in seconds
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Battle")


# Emulator options
options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat-pwm'
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.brightness = 100
options.pwm_bits = 11
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
matrix = RGBMatrix(options=options)

# Create an offscreen canvas to draw on
canvas = matrix.CreateFrameCanvas()

# Game variables
player1_x, player1_y = 0, 0
player2_x, player2_y = 31, 31
player_speed = 1

matrix = RGBMatrix(options=options)


# Player class


# Initialize grid
grid = [[(255, 255, 255) for _ in range(COLS)] for _ in range(ROWS)]

# Initialize players
player1 = Player(RED, (0, 0))
player2 = Player(BLUE, (COLS - 1, ROWS - 1))


def update_canvas(canvas, player1_x, player1_y, player2_x, player2_y):
    # Clear the canvas
    canvas.Clear()

    # Draw players
    canvas.SetPixel(player1_x, player1_y, 255, 0, 0)  # Red color for Player 1
    canvas.SetPixel(player2_x, player2_y, 0, 0, 255)  # Blue color for Player 2

    # Update the display
    # canvas = matrix.SwapOnVSync()  # Use SwapOnVSync to update the display


# Game loop
def main():
    running = True
    start_time = pygame.time.get_ticks()
    while running:
        # Check for game duration
        if pygame.time.get_ticks() - start_time > GAME_DURATION * 1000:
            running = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Player 1 movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1_y = (player1_y - player_speed) % options.rows
                elif event.key == pygame.K_s:
                    player1_y = (player1_y + player_speed) % options.rows
                elif event.key == pygame.K_a:
                    player1_x = (player1_x - player_speed) % options.cols
                elif event.key == pygame.K_d:
                    player1_x = (player1_x + player_speed) % options.cols

            # Player 2 movement (using arrow keys)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2_y = (player2_y - player_speed) % options.rows
                elif event.key == pygame.K_DOWN:
                    player2_y = (player2_y + player_speed) % options.rows
                elif event.key == pygame.K_LEFT:
                    player2_x = (player2_x - player_speed) % options.cols
                elif event.key == pygame.K_RIGHT:
                    player2_x = (player2_x + player_speed) % options.cols

        # Painting logic
        # ... (Add your painting logic here)

        # Update the canvas
        canvas.Clear()
        canvas.SetPixel(player1_x, player1_y, 255, 0, 0)  # Red color for Player 1
        canvas.SetPixel(player2_x, player2_y, 0, 0, 255)  # Blue color for Player 2
        canvas = matrix.SwapOnVSync(canvas)

        # Limit the frame rate
        pygame.time.Clock().tick(30)

    # Determine the winner
    winner = 'Player 1' if player1.cells_painted > player2.cells_painted else 'Player 2'
    print(f"{winner} wins!")

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
