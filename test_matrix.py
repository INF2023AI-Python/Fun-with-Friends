import pygame
#from rgbmatrix import RGBMatrix, RGBMatrixOptions
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions


# Set according to your RGB matrix dimensions
width, height = 32, 32

# Configuration for Matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'

matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Initialize Pygame
pygame.init()

# Set up gamepads
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Initialize game area
game_area = [[0 for _ in range(width)] for _ in range(height)]

# Player variables
player_size = 1
player1_x = width // 4
player1_y = height // 2
player1_speed = 1  # Adjusted the speed for better control
player1_color = (255, 0, 0)  # Red
player1_trail_color = (0, 255, 0)  # Green trail for Player 1 (weaker)

player2_x = 3 * width // 4
player2_y = height // 2
player2_speed = 1  # Adjusted the speed for better control
player2_color = (0, 0, 255)  # Blue
player2_trail_color = (255, 255, 0)  # Yellow trail for Player 2 (stronger)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 8:
                print("Button 8 pressed")
                running = False

    for i, joystick in enumerate(joysticks):
        pygame.event.pump()  # Pump the event queue to update joystick status

        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)
        print(f"Joystick {i + 1} - Axis X: {axis_x}, Axis Y: {axis_y}")

        if i == 0:  # Player 1 controls (First gamepad)
            player1_x += int(axis_x * player1_speed)
            player1_y += int(axis_y * player1_speed)
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)

    # Wrap player 1 around the screen borders
    player1_x %= width
    player1_y %= height

    # Wrap player 2 around the screen borders
    player2_x %= width
    player2_y %= height

    # Check for painting over and handle wrapping around the screen
    game_area[int(player1_y)][int(player1_x)] = 1  # Player 1
    game_area[int(player2_y)][int(player2_x)] = 2  # Player 2

    # Draw trails and players on offset_canvas
    offset_canvas.Clear()
    for y in range(height):
        for x in range(width):
            if game_area[y][x] == 1:
                offset_canvas.SetPixel(x, y, player1_trail_color[0], player1_trail_color[1], player1_trail_color[2])
            elif game_area[y][x] == 2:
                offset_canvas.SetPixel(x, y, player2_trail_color[0], player2_trail_color[1], player2_trail_color[2])

    offset_canvas.SetPixel(player1_x, player1_y, player1_color[0], player1_color[1], player1_color[2])
    offset_canvas.SetPixel(player2_x, player2_y, player2_color[0], player2_color[1], player2_color[2])

    # aktualisieren
    offset_canvas = matrix.SwapOnVSync(offset_canvas)

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
