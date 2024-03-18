from game_loop import player1_points, player2_points
from rgbmatrix import graphics
import pygame

# from RGBMatrixEmulator import graphics
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player1_points = 0
        self.player2_points = 0

    def update(self, duration):
        self.player1_points = player1_points
        self.player2_points = player2_points
        self.remaining_time = duration
        
        # Calculate the elapsed time since the start of the game
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        elapsed_time_seconds = elapsed_time_ms // 1000  # Convert milliseconds to seconds
        self.remaining_time = max(60 - elapsed_time_seconds, 0)  # Calculate remaining time

    def draw(self, offset_canvas):

        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")
        blau = (0,255,255)
        turquoise = (0,0,255)
        pointsColor = graphics.Color(*blau)
        timeColor = graphics.Color(*turquoise)

       # Draw player 1's points on the left side
        graphics.DrawText(offset_canvas, font, 1, SCREEN_HEIGHT, pointsColor, str(self.player1_points))

        # Draw player 2's points on the right side
        graphics.DrawText(offset_canvas, font, SCREEN_WIDTH - 4, SCREEN_HEIGHT, pointsColor, str(self.player2_points))

        # Draw remaining time in the middle
        remaining_seconds = self.remaining_time % 60
        time_text = f"{remaining_seconds:02d}"
        graphics.DrawText(offset_canvas, font, SCREEN_WIDTH // 2 - len(time_text) -2 // 2, SCREEN_HEIGHT, timeColor, time_text)
