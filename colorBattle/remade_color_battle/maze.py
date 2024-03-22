from rgbmatrix import RGBMatrix, RGBMatrixOptions
import random

# Initialize RGB Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat-pwm"
options.drop_privileges = 0
matrix = RGBMatrix(options=options)
offset_canvas = matrix.CreateFrameCanvas()

# Constants for maze size
MAZE_HEIGHT = 10
MAZE_WIDTH = 10

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def generate_maze(height, width):
    maze = [[0] * width for _ in range(height)]  # Initialize maze with walls

    # Randomly generate starting point and ending point
    start_row, start_col = random.randint(0, height - 1), random.randint(0, width - 1)
    end_row, end_col = random.randint(0, height - 1), random.randint(0, width - 1)

    # Set starting point and ending point as passage
    maze[start_row][start_col] = 1
    maze[end_row][end_col] = 1

    # Generate maze recursively
    generate_maze_recursive(maze, start_row, start_col)

    return maze, (start_row, start_col), (end_row, end_col)

def generate_maze_recursive(maze, row, col):
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Up, Down, Left, Right
    random.shuffle(directions)

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == 0:
            maze[new_row][new_col] = 1  # Set the cell as passage
            maze[row + dr // 2][col + dc // 2] = 1  # Break the wall between the cells
            generate_maze_recursive(maze, new_row, new_col)

def draw_maze(canvas, maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 0:
                canvas.SetPixel(col, row, *BLACK)  # Draw wall
            else:
                canvas.SetPixel(col, row, *WHITE)  # Draw passage

def main():
    while True:
        maze, _, _ = generate_maze(MAZE_HEIGHT, MAZE_WIDTH)
        draw_maze(offset_canvas, maze)
        matrix.SwapOnVSync(offset_canvas)

if __name__ == "__main__":
    main()
