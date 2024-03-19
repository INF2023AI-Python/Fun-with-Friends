# from game_loop import player1_points, player2_points
from rgbmatrix import graphics
import pygame
import time

# from RGBMatrixEmulator import graphics
SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32

class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas

        self.player1_points = 0
        self.player2_points = 0

        self.start_time = time.time()

        blau = (0,255,255)
        turquoise = (0,0,255)
        self.pointsColor = graphics.Color(*blau)
        self.timeColor = graphics.Color(*turquoise)

        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")

    def update(self, duration):
        # self.player1_points = player1_points
        # self.player2_points = player2_points
        # self.remaining_time = duration
        
        # Calculate the elapsed time since the start of the game
        elapsed_time = time.time - self.start_time
        remaining_time = duration - elapsed_time
        return remaining_time
    
    def draw(self, offset_canvas, duration):

        remaining_seconds = Scoreboard.update(self, duration)

       # Draw player 1's points on the left side
        graphics.DrawText(offset_canvas, self.font, 1, SCREEN_HEIGHT, self.pointsColor, str(self.player1_points))

        # Draw player 2's points on the right side
        graphics.DrawText(offset_canvas, self.font, SCREEN_WIDTH - 4, SCREEN_HEIGHT, self.pointsColor, str(self.player2_points))

        # Draw remaining time in the middle
        # remaining_seconds = self.remaining_time % 60
        time_text = f"{remaining_seconds:02d}"
        graphics.DrawText(offset_canvas, font, SCREEN_WIDTH // 2 - len(time_text) -2 // 2, SCREEN_HEIGHT, self.timeColor, time_text)
