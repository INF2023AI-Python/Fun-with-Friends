import pygame
pygame.init()
print("pygame initialized")
pygame.joystick.init()
print("joystick initialized")

# Check for available gamepads
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No gamepads detected")

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

# Setup screen
screen = pygame.display.set_mode((640, 640))
print("screen set mode")
pygame.display.set_caption("Screen Test")
print("screen set caption")

# Main loop for testing gamepads
running = True
clock = pygame.time.Clock()
print("clock initialized")
