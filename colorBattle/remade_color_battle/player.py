ROWS = 32
COLS = 32


class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.x, self.y = start_pos
        self.cells_painted = 0

    def move(self, direction):
        if direction == 'UP':
            self.y = (self.y - 1) % ROWS
        elif direction == 'DOWN':
            self.y = (self.y + 1) % ROWS
        elif direction == 'LEFT':
            self.x = (self.x - 1) % COLS
        elif direction == 'RIGHT':
            self.x = (self.x + 1) % COLS

    def paint(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color
            self.cells_painted += 1

    def repaint_trail(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color
