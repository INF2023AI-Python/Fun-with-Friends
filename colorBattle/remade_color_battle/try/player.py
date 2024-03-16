PLAY_WIDTH = 32
PLAY_HEIGHT = 28


class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.x, self.y = start_pos
        self.cells_painted = 0

    def move(self, direction):
        if direction == 'UP':
            self.y = (self.y - 1) % PLAY_WIDTH
        elif direction == 'DOWN':
            self.y = (self.y + 1) % PLAY_WIDTH
        elif direction == 'LEFT':
            self.x = (self.x - 1) % PLAY_HEIGHT
        elif direction == 'RIGHT':
            self.x = (self.x + 1) % PLAY_HEIGHT

    def paint(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color
            self.cells_painted += 1

    def repaint_trail(self, grid):
        if grid[self.y][self.x] != self.color:
            grid[self.y][self.x] = self.color
