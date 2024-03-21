PLAY_HEIGHT = 26
PLAY_WIDTH = 32


class Player:
    def __init__(self, color, trail_color, start_pos):
        self.color = color
        self.trail_color = trail_color
        self.x, self.y = start_pos
        self.cells_painted = 0
        self.trail = [start_pos]  # Initialize the trail with the start position

    def move(self, button, maze_pattern, game_area):
        if button == 0:  # Up
            new_y = (self.y - 1) % PLAY_HEIGHT
            if not self.is_collision(new_y, self.x, maze_pattern, game_area):
                self.y = new_y
                print("Up button pressed")
        elif button == 1:  # Right
            new_x = (self.x + 1) % PLAY_WIDTH
            if not self.is_collision(self.y, new_x, maze_pattern, game_area):
                self.x = new_x
                print("Right button pressed")
        elif button == 2:  # Down
            new_y = (self.y + 1) % PLAY_HEIGHT
            if not self.is_collision(new_y, self.x, maze_pattern, game_area):
                self.y = new_y
                print("Down button pressed")
        elif button == 3:  # Left
            new_x = (self.x - 1) % PLAY_WIDTH
            if not self.is_collision(self.y, new_x, maze_pattern, game_area):
                self.x = new_x
                print("Left button pressed")
        self.trail.append((self.x, self.y))

    def paint(self, canvas):
        # Check if the indices are within the range of the grid dimensions
        canvas.SetPixel(self.x, self.y, *self.trail_color)
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
            if self.y < len(grid) and self.x < len(grid[0]):
                grid[self.y][self.x] = self.trail_color
                self.cells_painted += 1