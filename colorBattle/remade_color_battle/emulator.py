import RGBMatrixEmulator


class Emulator:
    def __init__(self, rows, cols, hardware_mapping='adafruit-hat-pwm'):
        # Initialize RGBMatrix options
        options = RGBMatrixEmulator.RGBMatrixOptions()
        options.hardware_mapping = hardware_mapping
        options.rows = rows
        options.cols = cols

        # Create RGBMatrix and canvas
        self.matrix = RGBMatrixEmulator.RGBMatrix(options)
        self.canvas = self.matrix.CreateFrameCanvas()

    def update_canvas(self, player1_x, player1_y, player2_x, player2_y):
        # Clear the canvas
        self.canvas.Clear()

        # Draw players
        self.canvas.SetPixel(player1_x, player1_y, 255, 0, 0)  # Red color for Player 1
        self.canvas.SetPixel(player2_x, player2_y, 0, 0, 255)  # Blue color for Player 2

        # Update the display
        self.canvas = self.canvas.SwapOnVSync()
