import time
import pygame

pygame.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i, joystick in enumerate(joysticks):
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

            # Blau Button 0
            # Rot Button 1
            # Gelb Button 2
            # Grün Button 3
            # Links Button 4
            # Rechts Button 5
            # Select Button 8
            # Start Button 9
        if i == 0:  # Player 1 controls (First gamepad)
            #Axis
            player1_x += int(axis_x * player1_speed) #up, down
            player1_y += int(axis_y * player1_speed) #left, right
            #Buttons
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    #your code
                if event.button == 1:
                    #your code
                if event.button == 2:
                    #your code
                if event.button == 3:
                    #your code
                if event.button == 4:
                    #your code
                if event.button == 5:
                    #your code
                if event.button == 8:
                    #your code
                if event.button == 9:
                    #your code
                
        elif i == 1:  # Player 2 controls (Second gamepad)
            player2_x += int(axis_x * player2_speed)
            player2_y += int(axis_y * player2_speed)