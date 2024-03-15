class Scoreboard:
    def __init__(self, canvas):
        self.canvas = canvas
        self.player1_points = 0
        self.player2_points = 0
        self.remaining_time = 300  # Example: 300 seconds = 5 minutes

    def update(self, player1_points, player2_points, remaining_time):
        self.player1_points = player1_points
        self.player2_points = player2_points
        self.remaining_time = remaining_time

    def draw(self):
        # Clear the scoreboard area
        self.canvas.Clear()

        # Draw player 1's points on the left side
        self.canvas.DrawText(1, PLAY_HEIGHT + 1, self.player1_points, (255, 255, 255))

        # Draw player 2's points on the right side
        self.canvas.DrawText(PLAY_WIDTH - 9, PLAY_HEIGHT + 1, self.player2_points, (255, 255, 255))

        # Draw remaining time in the middle
        remaining_minutes = self.remaining_time // 60
        remaining_seconds = self.remaining_time % 60
        time_text = f"Time: {remaining_minutes:02d}:{remaining_seconds:02d}"
        self.canvas.DrawText(PLAY_WIDTH // 2 - len(time_text) // 2, PLAY_HEIGHT + 1, time_text, (255, 255, 255))

# Example usage:
# Assuming you have an 'offset_canvas' object representing your LED matrix canvas
scoreboard = Scoreboard(offset_canvas)

# Update the scoreboard with player points and remaining time
scoreboard.update(player1_points, player2_points, remaining_time)

# Draw the updated scoreboard
scoreboard.draw()