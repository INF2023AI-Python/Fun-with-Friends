import pygame 


PLAY_WIDTH = 32
PLAY_HEIGHT = 26


class Player:
    def __init__(self, color, trail_color, start_pos, game_area, maze_pattern):
        self.color = color
        self.trail_color = trail_color
        self.position = start_pos
        self.x_axis = 0
        self.y_axis = 0
        self.speed = 1
        self.maze_pattern = maze_pattern
        self.game_area = game_area

    def is_collision(self, x, y, level):
        # collision check, it ought to be added in move-function, to make sure the player will not cross the barriers
        if level == "hard":
            if self.maze_pattern[y][x] == "#":
                return True
        elif level == "easy":
            if self.game_area[y][x] == 1:
                return True
        return False
    
    def move(self, level, grid, canvas):
        # get current postion
        x = self.position[0]
        y = self.position[1]
        
        new_x = x
        new_y = y

        # calculate the amount of position change
        dx = round(self.x_axis * self.speed)
        dy = round(self.y_axis * self.speed)
        
        new_x = (x + dx) % PLAY_WIDTH
        new_y = (y + dy) % PLAY_HEIGHT

        # wrap the player in play field
        new_x = max(0, min(new_x, PLAY_WIDTH - 1))  
        new_y = max(0, min(new_y, PLAY_HEIGHT - 1)) 
        
        # check collision and update the new pos
        if not self.is_collision(new_y, new_x, level):
            x = new_x
            y = new_y
        else:
            new_x = x
            new_y = y
            

        # # gradually update position for smooth movement, to make it look like it move one pixel by one pixel
        # steps = max(abs(dx), abs(dy))
        # for i in range(steps):
        #     interp_x = round(x + (dx * i) / steps)
        #     interp_y = round(y + (dy * i) / steps)
        #     grid[interp_y][interp_x] = self.trail_color  # Update grid with trail color
        #     canvas.SetPixel(interp_x, interp_y, *self.trail_color) # paint the trail
        #     pygame.time.delay(5)  # a small delay for smooth movement
        
        grid[y][x] = self.trail_color  # Update grid with trail color
        canvas.SetPixel(x, y, *self.trail_color)
        # update position
        self.position = (new_x, new_y)
        

    def paint(self, canvas):
        # paint the postion of the player, trail and player color are not the same, in oder to identify the current position
        canvas.SetPixel(self.position[0], self.position[1], *self.color)
