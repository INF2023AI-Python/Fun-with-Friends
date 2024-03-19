from rgbmatrix import graphics
import time

SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player1_points = 0
        self.player2_points = 0
        self.start_time = time.time()

        blau = (0, 255, 255)
        turquoise = (0, 0, 255)
        self.pointsColor = graphics.Color(*blau)
        self.timeColor = graphics.Color(*turquoise)

        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")

    def update(self, duration):
        # self.player1_points = player1_points
        # self.player2_points = player2_points
        elapsed_time = time.time() - self.start_time
        remaining_time = max(duration - elapsed_time, 0)
        return remaining_time

    def draw(self, offset_canvas, duration):
        remaining_seconds = self.update(duration)

        # Draw player 1's points on the left side
        graphics.DrawText(offset_canvas, self.font, 1, SCREEN_HEIGHT, self.pointsColor, str(self.player1_points))

        # Draw player 2's points on the right side
        graphics.DrawText(offset_canvas, self.font, SCREEN_WIDTH - 4, SCREEN_HEIGHT, self.pointsColor, str(self.player2_points))

        # Draw remaining time in the middle
        time_text = f"{int(remaining_seconds):02d}"
        graphics.DrawText(offset_canvas, self.font, SCREEN_WIDTH // 2 - len(time_text) - 2 // 2, SCREEN_HEIGHT, self.timeColor, time_text)
