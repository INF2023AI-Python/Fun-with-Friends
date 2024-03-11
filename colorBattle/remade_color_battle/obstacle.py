import pygame

PLAY_WIDTH = 32
PLAY_HEIGHT = 28

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
    offset_canvas.Clear()

    # draw
    for y in range(PLAY_HEIGHT):
        for x in range(PLAY_WIDTH):
            if game_area[y][x] == 1:
                pygame.draw.rect(offset_canvas, obstacle_color, (x, y, 1, 1))

    # offset_canvas to refresh the screen, already in main
    offset_canvas = matrix.SwapOnVSync(offset_canvas)

