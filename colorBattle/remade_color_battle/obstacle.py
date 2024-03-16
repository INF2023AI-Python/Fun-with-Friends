import random
import pygame

# Constants in setting
PLAY_WIDTH = 32
PLAY_HEIGHT = 28
LINE_LENGTH = 2  # Adjust the length of the lines as needed
LINE_SPACING = 4  # Adjust the spacing between lines as needed
obstacle_color = (255, 255, 255)

def obstacle(offset_canvas, matrix):
    game_area = [[0 for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]
    obstacle_color = (255, 255, 255)
    # set the position for the obstacles, can change the number in needs
    line_y = 15
    line_x = 10
    for x in range(1, 5):
        game_area[line_y][x] = 1
    for x in range(7, 9):
        game_area[line_y][x] = 1
    for y in range(10, 20):
        game_area[y][line_x] = 1

    # clear
    # obstacle_color = (255, 255, 255)

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
    offset_canvas.Clear()

    # draw
    # Draw
    for y in range(PLAY_HEIGHT):
        for x in range(PLAY_WIDTH):
            if game_area[y][x] == 1:
                pygame.draw.rect(offset_canvas, obstacle_color, (x, y, 1, 1))
                # Draw a horizontal or vertical line
                if y + LINE_LENGTH <= PLAY_HEIGHT:
                    for i in range(LINE_LENGTH):
                        offset_canvas.SetPixel(x, y + i, obstacle_color[0], obstacle_color[1], obstacle_color[2])
                else:
                    for i in range(LINE_LENGTH):
                        offset_canvas.SetPixel(x + i, y, obstacle_color[0], obstacle_color[1], obstacle_color[2])

    # Update the matrix
    matrix.SwapOnVSync(offset_canvas)
    #or offset_canvas = matrix.SwapOnVSync(offset_canvas)

def maze(offset_canvas, matrix):
    # Clear
    offset_canvas.Clear()

    # Draw maze pattern
    maze_pattern = [
        "################################",
        "#                              #",
        "######## ##### #################",
        "#                 #            #",
        "##### ################ #########",
        "#       #                      #",
        "########### ##### ########### ##",
        "                                ",
        "######## ######## ######## #####",
        "#                 #            #",
        "# ######### ############# #### #",
        "#       #                      #",
        "########### ##### ########### ##",
        "                                ",
        "# ######### ############# #### #",
        "    #           #           #   ",
        "#       #             #         #",
        "######## ######## ######## #####",
        "#                 #            #",
        "# ######### ############# #### #",
        "#                              #",
        "######## ######## ######## #####",
        "#                 #            #",
        "########### ##### ########### ##",
        "#                              #",
        "######## ######## ######## #####",
        "#                              #",
        "################################",
    ]

    # offset_canvas to refresh the screen, already in main
    offset_canvas = matrix.SwapOnVSync(offset_canvas)
    for y, row in enumerate(maze_pattern):
        for x, cell in enumerate(row):
            if cell == "#":
                offset_canvas.SetPixel(x, y, obstacle_color[0], obstacle_color[1], obstacle_color[2])

    # Update the matrix
    matrix.SwapOnVSync(offset_canvas)

    return maze_pattern