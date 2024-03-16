import pygame
import emulator
from player import Player

# Constants
ROWS = 32
COLS = 32
PLAYER_SIZE = 1
PLAYER_SPEED = 1

# Initialize the emulator settings
emulator_settings.init_emulator(ROWS, COLS)

# Initialize players
player1 = Player((255, 0, 0), (1, 1))
player2 = Player((0, 0, 255), (COLS - 2, ROWS - 2))

# Main function
def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player positions
        player1.move()
        player2.move()

        # Paint trails
        player1.paint()
        player2.paint()

        # Update canvas
        emulator_settings.update_canvas(player1.x, player1.y, player2.x, player2.y)

        # Limit frame rate
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
