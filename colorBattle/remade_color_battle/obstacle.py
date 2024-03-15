import random

# Constants in setting
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
LINE_LENGTH = 2  # Adjust the length of the lines as needed
LINE_SPACING = 4  # Adjust the spacing between lines as needed
obstacle_color = (255, 255, 255)


def obstacle(offset_canvas, matrix):
    game_area = [[0 for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]

    # Create parallel horizontal lines
    for y in range(2, PLAY_HEIGHT, LINE_SPACING):
        x = random.randint(2, PLAY_WIDTH - LINE_LENGTH)
        game_area[y][x:x + LINE_LENGTH] = [1] * LINE_LENGTH

    # Create parallel vertical lines
    for x in range(2, PLAY_WIDTH, LINE_SPACING):
        y = random.randint(2, PLAY_HEIGHT - LINE_LENGTH)

        # Check if the vertical line will overlap with a horizontal line
        while any(game_area[y + i][x] == 1 for i in range(LINE_LENGTH)):
            y = random.randint(2, PLAY_HEIGHT - LINE_LENGTH)

        for i in range(LINE_LENGTH):
            game_area[y + i][x] = 1

    # Clear
    offset_canvas.clear()

    # Draw
    for y in range(PLAY_HEIGHT):
        for x in range(PLAY_WIDTH):
            if game_area[y][x] == 1:
                # Draw a horizontal or vertical line
                if y + LINE_LENGTH <= PLAY_HEIGHT:
                    for i in range(LINE_LENGTH):
                        offset_canvas.SetPixel(x, y + i, obstacle_color[0], obstacle_color[1], obstacle_color[2])
                else:
                    for i in range(LINE_LENGTH):
                        offset_canvas.SetPixel(x + i, y, obstacle_color[0], obstacle_color[1], obstacle_color[2])

    # Update the matrix
    matrix.SwapOnVSync(offset_canvas)

    # Return the game area
    return game_area
