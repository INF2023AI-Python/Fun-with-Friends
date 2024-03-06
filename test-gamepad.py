#!/usr/bin/env python

import os, sys, pygame 
from pygame import locals
import time

# Define the colors we will use in RGB format
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

while done:
    for e in pygame.event.get():  # iterate over event stack
        if e.type == pygame.QUIT:
            done = False

        if e.type == pygame.locals.JOYAXISMOTION:  # Read Analog Joystick Axis
            x1, y1 = j.get_axis(0), j.get_axis(1)  # Left Stick

            print(x1)
            print(y1)
            x1Text = textfont.render("x : " + str(x1), 1, red)
            y1Text = textfont.render("y : " + str(y1), 1, red)
            pygame.draw.rect(screen, black, (1, 1, matrix_resolution[0] * 2 - 2, matrix_resolution[1] * 2 - 2), 0)
            pygame.draw.rect(screen, white, (matrix_resolution[0] + int(x1 * 16), matrix_resolution[1] + int(y1 * 16), 4, 4), 0)
            pygame.draw.rect(screen, white, (matrix_resolution[0] * 2, matrix_resolution[1] * 3, matrix_resolution[0] * 2, matrix_resolution[1] * 2), 0)
            screen.blit(x1Text, (matrix_resolution[0] * 6, matrix_resolution[1] * 3))
            screen.blit(y1Text, (matrix_resolution[0] * 6, matrix_resolution[1] * 4))
            pygame.display.flip()

        if e.type == pygame.locals.JOYBUTTONDOWN:  # Read the buttons
            print("button down" + str(e.button))
            for i in range(0, 10):
                if e.button == i:
                    pygame.draw.rect(screen, red, (matrix_resolution[0] * 2 + i * 2, matrix_resolution[1] * 2, 2, 2), 0)
                    buttonText = textfont.render(str(i), 1, white)
                    screen.blit(buttonText, (matrix_resolution[0] * 2 + i * 2 + 1, matrix_resolution[1] * 2))
                    pygame.display.flip()

        if e.type == pygame.locals.JOYBUTTONUP:  # Read the buttons
            print("button up" + str(e.button))
            for i in range(0, 10):
                if e.button == i:
                    pygame.draw.rect(screen, white, (matrix_resolution[0] * 2 + i * 2, matrix_resolution[1] * 2, 2, 2), 0)
                    pygame.display.flip()
