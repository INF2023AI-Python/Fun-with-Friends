import random
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time


def random_direction():
    """
    This method returns a random direction that the snake can move in.
    The directions are represented as tuples, where (0, -1) represents up, (0, 1) represents down,
    (-1, 0) represents left, and (1, 0) represents right.
    You should replace this with the correct logic for your joystick.
    """
    return random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])

# Displaying text in the matrix
def display_text(text, color, offset_canvas, matrix):
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


class Snake:
    def __init__(self):
        """ The constructor of the Snake class.
        It initializes the snake with a length of 1 and sets its initial
         position to the middle of the screen.
        It also sets the initial direction of the snake to a
         random direction and the color of the snake to blue.
        """
        self.length = 4
        self.positions = [(32 // 2, 32 // 2)] * self.length
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
        new = ((cur[0] + x) % 32, (cur[1] + y) % 32)
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
        self.positions = [((32 // 2), (32 // 2))]
        self.direction = random_direction()

    def draw(self, matrix):
        """ This method draws the snake on the screen.
        It uses the pygame.draw.rect function to draw each segment of
        the snake as a rectangle. """
        for p in self.positions:
            matrix.SetPixel(p[0], p[1], self.color[0], self.color[1], self.color[2])


class Game:
    def __init__(self, offset_canvas, matrix):
        self.offset_canvas = offset_canvas
        self.matrix = matrix
        pygame.init()
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.fruit = Fruit()
        self.start_time = time.time()
        self.game_over_flag = False

    def draw(self, offset_canvas, matrix):
        """
        This method handles rendering the game state to the matrix.
        It clears the matrix, then draws the snake and the fruit.
        """

        # Clear the canvas
        matrix.Clear()

        # Draw the snake
        self.snake.draw(offset_canvas)

        # Draw the fruit
        if self.fruit is not None:
            self.fruit.draw(offset_canvas)

        # Swap the buffers
        matrix.SwapOnVSync(self.offset_canvas)

    def update(self, matrix):
        """
        This method handles updating the game state.
        It moves the snake and checks if the snake has eaten the fruit or collided with itself.
        """
        if self.game_over_flag:
            return
        
        if not self.snake.move():
            matrix.Clear()
            color = (255, 0, 0)
            display_text(["Snake", "ate", "itself"], color, self.offset_canvas, matrix)
            time.sleep(3)
            print("The snake ate itself!")
            self.game_over(matrix)
            return

        head_position = self.snake.get_head_position()

        if self.fruit and head_position == self.fruit.position:
            self.snake.length += 1
            self.fruit = None  # Remove the current fruit

        if self.fruit is None:
            self.fruit = Fruit()

        if time.time() - self.start_time > 60:
            matrix.Clear()
            color = (255, 0, 0)
            display_text(["Time","is", "up!"], color, self.offset_canvas, matrix)
            time.sleep(3)
            print("Time's up!")
            self.game_over(matrix)
            return

    def game_over(self, matrix):
        # Display "Game Over" on the matrix and stop the game
        # matrix.Fill(255, 0, 0)
        print("Game Over line 168")
        #pygame.quit()
        matrix.Clear()
        self.game_over_flag = True
        return

    def handle_events(self, matrix):
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
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    print("back to start")
                    matrix.Clear()
                    self.game_over_flag = True
                    return

    def run(self, offset_canvas, matrix):
        """
        This method runs the main game loop.
        It repeatedly handles events, updates the game state, and draws the new game state to the screen.
        """
        while True:
            self.handle_events(matrix)
            self.update(matrix)
            self.draw(offset_canvas, matrix)
            if self.game_over_flag:
                print("Game Over")
                matrix.Clear()
                return
            self.clock.tick(10)


class Fruit:
    def __init__(self):
        self.position = (random.randint(0, 32 - 1), random.randint(0, 32 - 1))
        self.color = random.choice([(255, 0, 0), (0, 255, 0)])  # Red or green

    def draw(self, matrix):
        matrix.SetPixel(self.position[0], self.position[1], self.color[0], self.color[1], self.color[2])


def snake(offset_canvas, matrix):
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        print("No joystick found.")
        return
    
    game = Game(offset_canvas, matrix)
    game.run(offset_canvas, matrix)