# from game_loop import player1_points, player2_points
from rgbmatrix import graphics

SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player1_points = 0
        self.player2_points = 0

    def update(self, duration):
        # self.player1_points = player1_points
        # self.player2_points = player2_points
        self.remaining_time = duration
        
        # Update remaining time
        # Decrement remaining time each frame
        self.remaining_time -= 1
        # Ensure remaining time doesn't go below 0
        if self.remaining_time < 0:
            self.remaining_time = 0

    def draw(self):
        # Clear the scoreboard area
        self.canvas.Clear()

        # Create graphics context
        offscreen_canvas = self.canvas
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")

        points_color = (0,255,255)
        time_color = (0,0,255)
        pointsColor = graphics.Color(*points_color)
        timeColor = graphics.Color(*time_color)



        # Draw player 1's points on the left side
        graphics.DrawText(offscreen_canvas, font, 1, SCREEN_HEIGHT, pointsColor, str(self.player1_points))

        # Draw player 2's points on the right side
        graphics.DrawText(offscreen_canvas, font, SCREEN_WIDTH - 9, SCREEN_HEIGHT, pointsColor, str(self.player2_points))

        # Draw remaining time in the middle
        remaining_seconds = self.remaining_time % 60
        time_text = f"{remaining_seconds:02d}"
        graphics.DrawText(offscreen_canvas, font, SCREEN_WIDTH-len(time_text), SCREEN_HEIGHT, timeColor, time_text)

    # def draw(self):
    #     # Clear the scoreboard area
    #     self.canvas.Clear()

    #     # Draw player 1's points on the left side
    #     graphics.DrawText(1, PLAY_HEIGHT + 1, self.player1_points, (0,255,255))

    #     # Draw player 2's points on the right side
    #     graphics.DrawText(PLAY_WIDTH - 9, PLAY_HEIGHT + 1, self.player2_points, (0,255,255))

    #     # Draw remaining time in the middle
    #     remaining_seconds = self.remaining_time % 60
    #     time_text = f"{remaining_seconds:02d}"
    #     self.canvas.DrawText(PLAY_WIDTH // 2 - len(time_text) // 2, PLAY_HEIGHT + 1, time_text, (0,0,255))


# scoreboard = Scoreboard(offset_canvas)

# # Update the scoreboard with player points and remaining time
# scoreboard.update(player1_points, player2_points, remaining_time)

# # Draw the updated scoreboard
# scoreboard.draw()