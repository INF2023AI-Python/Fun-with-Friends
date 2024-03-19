# from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

ROWS = 32
COLS = 32


class Emulator:
    def __init__(self, rows, cols, hardware_mapping='adafruit-hat-pwm'):
        # Initialize RGBMatrix options
        options = RGBMatrixOptions()
        options.hardware_mapping = hardware_mapping
        options.rows = rows
        options.cols = cols
        options.drop_privileges = 0

        # Create RGBMatrix and canvas
        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def update_canvas(self, grid):
        # Clear the canvas
        self.canvas.Clear()

        # Draw the game state
        for i in range(ROWS):
            for j in range(COLS):
                color = grid[i][j]
                self.canvas.SetPixel(i, j, *color)

        # Update the display
        self.matrix.SwapOnVSync(self.canvas)
