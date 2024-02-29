#import board
#import neopixel
#import time


import pygame
#from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

#Konfiguration der Matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options = options)

offset_canvas = matrix.CreateFrameCanvas()

#Initialisierung von Pygame
pygame.init()

# Einrichten des Bildschirms (nicht notwendig, aber Pygame erfordert es)
screen = pygame.display.set_mode((100, 100))

# Erkennen eines Controllers
pygame.joystick.init()
controller_count = pygame.joystick.get_count()

# Endlosschleife zum Lesen der Eingaben
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            print("Taste", event.button, "gedrückt")
        elif event.type == pygame.JOYBUTTONUP:
            print("Taste", event.button, "freigegeben")



#Ausgabe des Spielfeldes    
def printGrid4 ():
    a = 6
    while a < 27:

        b = 8
        while b < 24:  
            offset_canvas.SetPixel(b, a, 255, 0, 0)
            offset_canvas = matrix.SwapOnVSync(offset_canvas)
            b += 1
    
        a += 9

    c = 6
    while c<27:
        offset_canvas.SetPixel(25, c, 255, 255, 255)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)
        c += 1



#Ausgabe eines neuen Chips
#def newChip4(colorP1, colorP2, x1, x2, y1, y2):
    #numberMoves #Variable, die die Züge der Spieler zählt und den aktuellen Zug enthält
    #if numberMoves%2 == 1:
        #offset_canvas.SetPixel(x1, y1, (colorP1))
        #offset_canvas.SetPixel(x2, y1, (colorP1))
        #offset_canvas.SetPixel(x1, y2, (colorP1))
        #offset_canvas.SetPixel(x2, y2, (colorP1))

    #if numberMoves%2 == 0:
        #offset_canvas.SetPixel(x1, y1, (colorP2))
        #offset_canvas.SetPixel(x2, y1, (colorP2))
        #offset_canvas.SetPixel(x1, y2, (colorP2))
        #offset_canvas.SetPixel(x2, y2, (colorP2))



#Löschen der alten Chips
#def deleteChip(x1, x2, y1, y2):
    #offset_canvas.SetPixel(x1, y1, (0, 0, 0))
    #offset_canvas.SetPixel(x2, y1, (0, 0, 0))
    #offset_canvas.SetPixel(x1, y2, (0, 0, 0))
    #offset_canvas.SetPixel(x2, y2, (0, 0, 0))



#Farbgebung der Spieler und Chips
def color4():
    inputP1 = input("Spieler 1, sollen deine Chips rot, blau oder gruen sein?:")
    if inputP1 is "rot":
        colorP1 = (255, 0, 0)
    if inputP1 is "gruen":
        colorP1 = (0, 255, 0)
    if inputP1 is "blau":
        colorP1 = (0, 0, 255)
    else:
        print("Falsche Eingabe!")

    inputP2 = input("Spieler 2, sollen deine Chips rot, blau oder gruen sein?:")
    if inputP1 != inputP2:
        if inputP2 is "rot":
            colorP2 = (255, 0, 0)
        if inputP2 is "gruen":
            colorP2 = (0, 255, 0)
        if inputP2 is "blau":
            colorP2 = (0, 0, 255)
        else:
            print("Falsche Eingabe!")
    else:
        print("Ihr könnt nicht die gleiche Farbe haben!")
    
    colDecision4(colorP1, colorP2)
    


#Auswahl der Spalte
def colDecision4(colorP1, colorP2):
    #definition in der main zu Beginn?
    
    x1 = 4
    x2 = 5
    y1 = 7
    y2 = 8
    #newChip4(colorP1, colorP2, x1, x2, y1, y2)
    #if rechts and (y1<24):
       # deleteChip(x1, x2, y1, y2)
        #y1 += 3
        #y2 += 3
        #newChip4(colorP1, colorP2, x1, x2, y1, y2)
    #if links and (y1>5):
        #deleteChip(x1, x2, y1, y2)
        #y1 -= 3
        #y2 -= 3
        #newChip4(colorP1, colorP2, x1, x2, y1, y2)   


a = 6
while a < 28:

    b = 8
    while b < 26: 
        offset_canvas.SetPixel(a, b, 255, 255, 255)  
        offset_canvas = matrix.CreateFrameCanvas(offset_canvas)
        b += 3
    
    a += 1

c = 6
while c < 28:
    offset_canvas.SetPixel(25, c, 255, 255, 255)
    offset_canvas = matrix.CreateFrameCanvas(offset_canvas)
    c += 1

# Pygame beenden
pygame.quit()
