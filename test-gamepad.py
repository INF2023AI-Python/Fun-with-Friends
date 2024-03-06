 Define the colors we will use in RGB format
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

# Set the resolution for the 32x32 RGB matrix
matrix_resolution = [32, 32]

# Adjust the screen size accordingly
size = [matrix_resolution[0] * 20, matrix_resolution[1] * 10]
screen = pygame.display.set_mode(size)

# Fill the screen with white
screen.fill(white)

# Put something in the application Bar
pygame.display.set_caption("Testing gamepad")

pygame.draw.rect(screen, black, (1, 1, matrix_resolution[0] * 2 - 2, matrix_resolution[1] * 2 - 2), 0)

pygame.display.flip()

pygame.joystick.init()  # main joystick device system

textfont = pygame.font.SysFont("moonspace", 1)
joyfont = pygame.font.SysFont("moonspace", 3)

done = True

try:
    j = pygame.joystick.Joystick(0)  # create a joystick instance
    j.init()  # init instance
    print('Enabled joystick: ' + j.get_name())
    joyName = j.get_name()
except pygame.error:
    print('no joystick found.')

pygame.draw.rect(screen, black, (1, 1, matrix_resolution[0] * 2 - 2, matrix_resolution[1] * 2 - 2), 0)
pygame.draw.rect(screen, white, (matrix_resolution[0], matrix_resolution[1], 4, 4), 0)
joyText = textfont.render("Gamepad : " + joyName, 1, red)
screen.blit(joyText, (matrix_resolution[0] * 6, matrix_resolution[1] * 2))

pygame.display.flip()

