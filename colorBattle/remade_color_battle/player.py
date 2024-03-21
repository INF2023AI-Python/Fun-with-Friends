PLAY_HEIGHT = 26
PLAY_WIDTH = 32


class Player:
    def __init__(self, color, trail_color_rgb, start_pos):
        self.color = color
        self.trail_color_rgb = trail_color_rgb
        self.position = start_pos
        self.trail = [start_pos]  # Initialize the trail with the start position
        self.cells_painted = 0

    def move(self, x_axis, y_axis, maze_pattern, game_area):
        x, y = self.position
        new_x, new_y = x, y

        # Adjust the position based on gamepad input
        if abs(x_axis) > 0.5:
            new_x = (x + int(x_axis)) % PLAY_WIDTH
        if abs(y_axis) > 0.5:
            new_y = (y + int(y_axis)) % PLAY_HEIGHT
        
        if not self.is_collision(new_y, new_x, maze_pattern, game_area):
            self.position = (new_x, new_y)
            self.trail.append(self.position)

    def paint(self, canvas):
        # Check if the indices are within the range of the grid dimensions
        x, y = self.position
        canvas.SetPixel(x, y, *self.trail_color_rgb)
        self.cells_painted += 1

    def repaint_trail(self, canvas):
        # Check if the indices are within the range of the grid dimensions
        for x, y in self.trail:
            canvas.SetPixel(x, y, *self.color)

    def is_collision(self, y, x, maze_pattern, game_area):
        # Check if the indices are within the range of the grid dimensions
        if y < len(maze_pattern) and x < len(maze_pattern[0]):
            if maze_pattern[y][x] == "#":
                return True
            if game_area[y][x] == 1:
                return True
        return False
    
    def update_state(self, grid):
        # Update the game state based on the player's position and color
        x, y = self.position
        if y < len(grid) and x < len(grid[0]):
            grid[y][x] = self.trail_color_rgb
            self.cells_painted += 1
