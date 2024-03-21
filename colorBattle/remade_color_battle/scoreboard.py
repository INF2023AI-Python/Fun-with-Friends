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

        # Initialize variables to store the position and size of the time text area
        self.time_text_x = 0
        self.time_text_y = 0
        self.time_text_width = 0

    def update(self, duration):
        elapsed_time = int(time.time() - self.start_time)
        remaining_seconds = max(duration - elapsed_time, 0)
        time.sleep(1)
        return remaining_seconds

    def clear_time_text_area(self, offset_canvas):
    # Clear the area occupied by the previous time text using black color
        for x in range(32):
            for y in range(26, 32):
                offset_canvas.SetPixel(x, y, 0, 0, 0)  # Set pixel to black

    def draw(self, offset_canvas, duration):
        remaining_seconds = self.update(duration)
        print("Remaining Time:", remaining_seconds)  # Check the remaining time in the console

        # Clear the area occupied by the previous time text
        self.clear_time_text_area(offset_canvas)

        # Draw player 1's points on the left side
        graphics.DrawText(offset_canvas, self.font, 1, SCREEN_HEIGHT, self.pointsColor, str(self.player1_points))

        # Draw player 2's points on the right side
        graphics.DrawText(offset_canvas, self.font, SCREEN_WIDTH - 4, SCREEN_HEIGHT, self.pointsColor, str(self.player2_points))

        # Draw remaining time in the middle
        time_text = f"{int(remaining_seconds):02d}"
        self.time_text_width = len(time_text) * 3  # Calculate the width of the time text
        self.time_text_x = SCREEN_WIDTH // 2 - self.time_text_width // 2  # Calculate the x-coordinate of the time text
        self.time_text_y = SCREEN_HEIGHT  # Set the y-coordinate of the time text
        graphics.DrawText(offset_canvas, self.font, self.time_text_x, self.time_text_y, self.timeColor, time_text)

        return remaining_seconds