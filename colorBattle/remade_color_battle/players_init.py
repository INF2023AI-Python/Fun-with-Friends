SCREEN_WIDTH = 32
SCREEN_HEIGHT = 32


# The function to initialize players, setting their speed, size, color
def players_init():

    players_size = 1

    # Player 1
    player1_x = SCREEN_WIDTH // 4  # start position
    player1_y = SCREEN_HEIGHT // 4
    player1_speed = 10
    # Player1 - red
    player1_color = (255, 0, 0)
    # Trail1 - green
    player1_trail_color = (0, 255, 0)

    # Player 2

    player2_x = 3 * SCREEN_WIDTH // 4  # start position
    player2_y = SCREEN_HEIGHT // 2
    player2_speed = 10
    # Player2 - blue
    player2_color = (0, 0, 255)
    # Trail2 - yellow
    player2_trail_color = (255, 255, 0)

    return {
            'player_size': players_size,
            'player1_x': player1_x,
            'player1_y': player1_y,
            'player1_speed': player1_speed,
            'player1_color': player1_color,
            'player1_trail_color': player1_trail_color,
            'player2_x': player2_x,
            'player2_y': player2_y,
            'player2_speed': player2_speed,
            'player2_color': player2_color,
            'player2_trail_color': player2_trail_color
        }

