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
    maze = [['#'] * width for _ in range(height)]  # Initialize maze with walls

    # Randomly generate starting point and ending point
    start_row, start_col = random.randint(0, height - 1), random.randint(0, width - 1)
    end_row, end_col = random.randint(0, height - 1), random.randint(0, width - 1)

    # Set starting point and ending point as passage
    maze[start_row][start_col] = 'S'
    maze[end_row][end_col] = 'E'

    # Generate maze recursively
    generate_maze_recursive(maze, start_row, start_col)

    return maze, (start_row, start_col), (end_row, end_col)

def generate_maze_recursive(maze, row, col):
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Up, Down, Left, Right
    random.shuffle(directions)

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == '#':
            maze[new_row][new_col] = ' '  # Set the cell as passage
            maze[row + dr // 2][col + dc // 2] = ' '  # Break the wall between the cells
            generate_maze_recursive(maze, new_row, new_col)

# Display the maze on the RGB matrix
def draw_maze(canvas, maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == '#':
                canvas.SetPixel(col, row, 0, 0, 0)  # Draw wall
            elif maze[row][col] == 'S':
                canvas.SetPixel(col, row, 255, 255, 0)  # Draw start point
            elif maze[row][col] == 'E':
                canvas.SetPixel(col, row, 0, 255, 255)  # Draw end point
            else:
                canvas.SetPixel(col, row, 255, 255, 255)  # Draw passage
        
maze, _, _ = generate_maze(26, 32)
draw_maze(offset_canvas, maze)

def main():
    while True:
        matrix.SwapOnVSync(offset_canvas)

if __name__ == "__main__":
    main()