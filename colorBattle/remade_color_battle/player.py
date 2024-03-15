PLAY_HEIGHT = 28
PLAY_WIDTH = 32


class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.x, self.y = start_pos
        self.cells_painted = 0

    def move(self, direction, maze_pattern, game_area):
        if direction == 'UP':
            new_y = (self.y - 1) % PLAY_HEIGHT
            if not self.is_collision(new_y, self.x, maze_pattern, game_area):
                self.y = new_y
        elif direction == 'DOWN':
            new_y = (self.y + 1) % PLAY_HEIGHT
            if not self.is_collision(new_y, self.x, maze_pattern, game_area):
                self.y = new_y
        elif direction == 'LEFT':
            new_x = (self.x - 1) % PLAY_WIDTH
            if not self.is_collision(self.y, new_x, maze_pattern, game_area):
                self.x = new_x
        elif direction == 'RIGHT':
            new_x = (self.x + 1) % PLAY_WIDTH
            if not self.is_collision(self.y, new_x, maze_pattern, game_area):
                self.x = new_x

    def paint(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color
            self.cells_painted += 1

    def repaint_trail(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color

    def is_collision(self, y, x, maze_pattern, game_area):
        # Check if the indices are within the range of the grid dimensions
        if y < len(maze_pattern) and x < len(maze_pattern[0]):
            if maze_pattern[y][x] == "#":
                return True
            if game_area[y][x] == 1:
                return True
        return False
