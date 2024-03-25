from rgbmatrix import graphics

def winner(player1_points, player2_points):
    #define the winner
    player1 = ["Player", "1", "Won"]
    player2 = ["Player", "2", "Won"]
    tie = ["It's", "A", "Tie"]
    if player1_points > player2_points:
        return player1
    elif player2_points > player1_points:
        return player2
    else:
        return tie
def display_text(text, color, offset_canvas, matrix):
    #display end page: who wins
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
    textColor = graphics.Color(*color)

    # Text in the first line
    graphics.DrawText(offset_canvas, font, 2, 10, textColor, text[0])
    # Text in the second line
    graphics.DrawText(offset_canvas, font, 2, 20, textColor, text[1])
    # Text in the third line
    graphics.DrawText(offset_canvas, font, 2, 30, textColor, text[2])

    matrix.SwapOnVSync(offset_canvas)