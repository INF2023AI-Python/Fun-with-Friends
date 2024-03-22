import random
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

ROWS = 32
COLS = 32

options = RGBMatrixOptions()
options.cols = ROWS
options.rows = COLS
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)


# offset_canvas = matrix.CreateFrameCanvas()


def random_direction():
    """
    This method returns a random direction that the snake can move in.
    The directions are represented as tuples, where (0, -1) represents up, (0, 1) represents down,
    (-1, 0) represents left, and (1, 0) represents right.
    You should replace this with the correct logic for your joystick.
    """
    return random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])


class Snake:
    def __init__(self):
        """ The constructor of the Snake class.
        It initializes the snake with a length of 1 and sets its initial
         position to the middle of the screen.
        It also sets the initial direction of the snake to a
         random direction and the color of the snake to blue.
        """
        self.length = 4
        self.positions = [(ROWS // 2, COLS // 2)] * self.length
        self.direction = random_direction()
        self.next_direction = self.direction
        self.color = (0, 0, 255)

    def get_head_position(self):
        # This method returns the current position of the head of the snake.
        return self.positions[0]

    def turn(self, point):
        """
        This method changes the direction of the snake.
        It takes a point as an argument, which represents the new direction.
        If the new direction is not the opposite of the current direction
        (to prevent the snake from moving backwards into itself),
        it sets the direction of the snake to the new direction.
        """
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.next_direction = point

    def move(self):
        """
        This method updates the position of the snake based on its current
        direction.
        If the new position would cause the snake to run into itself,
        it resets the snake.
        Otherwise, it adds the new position to the list of positions and
        removes the last position if the length of the positions list is
        greater than the length of the snake.
        """
        self.direction = self.next_direction  # Update the direction before moving
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % ROWS, (cur[1] + y) % COLS)
        if new in self.positions:
            print("The snake ate itself!")
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        # This method resets the snake to its initial state.
        self.length = 1
        self.positions = [((ROWS // 2), (COLS // 2))]
        self.direction = random_direction()

    def draw(self, matrix):
        """ This method draws the snake on the screen.
        It uses the pygame.draw.rect function to draw each segment of
        the snake as a rectangle. """
        for p in self.positions:
            matrix.SetPixel(p[0], p[1], self.color[0], self.color[1], self.color[2])


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.fruit = Fruit()
        self.start_time = time.time()

    def draw(self):
        """
        This method handles rendering the game state to the matrix.
        It clears the matrix, then draws the snake and the fruit.
        """
        # Create a new off-screen buffer (canvas)
        canvas = matrix.CreateFrameCanvas()

        # Clear the canvas
        canvas.Clear()

        # Draw the snake
        self.snake.draw(canvas)

        # Draw the fruit
        if self.fruit is not None:
            self.fruit.draw(canvas)

        # Swap the buffers
        matrix.SwapOnVSync(canvas)

    def update(self):
        """
        This method handles updating the game state.
        It moves the snake and checks if the snake has eaten the fruit or collided with itself.
        """
        if not self.snake.move():
            print("The snake ate itself!")
            self.game_over()
            return

        head_position = self.snake.get_head_position()

        if self.fruit and head_position == self.fruit.position:
            self.snake.length += 1
            self.fruit = None  # Remove the current fruit

        if self.fruit is None:
            self.fruit = Fruit()

        if time.time() - self.start_time > 60:
            print("Time's up!")
            self.game_over()
            return

    def game_over(self):
        # Display "Game Over" on the matrix and stop the game
        # matrix.Fill(255, 0, 0)
        print("Game Over")
        pygame.quit()

    def handle_events(self):
        """
        This method handles user input.
        It checks for quit events and joystick movements, and turns the snake accordingly.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5 and self.snake.direction != (1, 0):
                        self.snake.turn((-1, 0))
                    elif event.value > 0.5 and self.snake.direction != (-1, 0):
                        self.snake.turn((1, 0))
                elif event.axis == 1:
                    if event.value < -0.5 and self.snake.direction != (0, 1):
                        self.snake.turn((0, -1))
                    elif event.value > 0.5 and self.snake.direction != (0, -1):
                        self.snake.turn((0, 1))

    def run(self):
        """
        This method runs the main game loop.
        It repeatedly handles events, updates the game state, and draws the new game state to the screen.
        """
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(3)


class Fruit:
    def __init__(self):
        self.position = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        self.color = random.choice([(255, 0, 0), (0, 255, 0)])  # Red or green

    def draw(self, matrix):
        matrix.SetPixel(self.position[0], self.position[1], self.color[0], self.color[1], self.color[2])


def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        print("No joystick found.")
        return

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
