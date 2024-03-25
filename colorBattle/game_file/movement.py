import pygame 
from obstacle import maze_pattern, game_area

PLAY_WIDTH = 32
PLAY_HEIGHT = 26


class Player:
    def __init__(self, color, trail_color, start_pos):
        self.color = color
        self.trail_color = trail_color
        self.position = start_pos
        self.x_axis = 0
        self.y_axis = 0
        self.speed = 2

    def is_collision(self, x, y, level):
        # collision check, it ought to be added in move-function, to make sure the player will not cross the barriers
        if level == "hard":
            if maze_pattern[y][x] == "#" or game_area[y][x] == 1:
                return True
        elif level == "easy":
            if game_area[y][x] == 1:
                return True
        return False
    
    def move(self, level, grid, canvas):
        # get current postion
        x = self.position[0]
        y = self.position[1]
        
        # calculate the amount of position change
        dx = round(self.x_axis * self.speed)
        dy = round(self.y_axis * self.speed)

        # check collision and update the new pos
        if not self.is_collision(new_y, new_x, level):
            new_x = (x + dx) % PLAY_WIDTH
            new_y = (y + dy) % PLAY_HEIGHT
        else:
            new_x = x
            new_y = y
            
        # wrap the player in play field
        new_x = max(0, min(new_x, PLAY_WIDTH - 1))  
        new_y = max(0, min(new_y, PLAY_HEIGHT - 1)) 

        # gradually update position for smooth movement, to make it look like it move one pixel by one pixel
        steps = max(abs(dx), abs(dy))
        for i in range(steps):
            interp_x = round(x + (dx * i) / steps)
            interp_y = round(y + (dy * i) / steps)
            grid[interp_y][interp_x] = self.trail_color  # Update grid with trail color
            canvas.SetPixel(interp_x, interp_y, *self.trail_color) # paint the trail
            pygame.time.delay(5)  # a small delay for smooth movement
        
        # update position
        self.position = (new_x, new_y)
        

    def paint(self, canvas):
        # paint the postion of the player, trail and player color are not the same, in oder to identify the current position
        canvas.SetPixel(self.position[0], self.position[1], *self.color)
