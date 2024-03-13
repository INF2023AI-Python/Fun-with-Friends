import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import subprocess
import psutil

orange_square_position = [0, 0]

# Konfiguration der Matrix
options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = 0
matrix = RGBMatrix(options=options)

# Funktion zum Löschen des Bildschirms
def clear_screen():
    matrix.Clear()

# Funktion zum Zeichnen der Piktogramme
def draw_pictograms():
    # Colorbattel
    for row in range(2, 7):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *red)
    for row in range(9, 14):
        for col in range(5, 10):
            matrix.SetPixel(row, col, *blue)

    # tictactoe
    positionsX = [
        (17, 4), (18, 5), (19, 6), (20, 7), (21, 6), (22, 5), (23, 4),
        (19, 8), (21, 8), (18, 9), (22, 9), (17, 10), (23, 10)
    ]
    for pos in positionsX:
        matrix.SetPixel(pos[0], pos[1], *red)
    positionsO = [
        (24, 6), (24, 7), (24, 8), (25, 5), (25, 9), (26, 4), (26, 10),
        (27, 4), (27, 10), (28, 5), (28, 9), (29, 6), (29, 7), (29, 8)
    ]
    for pos in positionsO:
        matrix.SetPixel(pos[0], pos[1], *blue)

    # VierGewinnt
    for row in range(2, 5):
        for col in range(27, 30):
            matrix.SetPixel(row, col, *red)
    for row in range(5, 8):
        for col in range(24, 30):
            matrix.SetPixel(row, col, *blue)
    for row in range(8, 11):
        for col in range(21, 30):
            matrix.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(18, 24):
            matrix.SetPixel(row, col, *blue)
    for row in range(11, 14):
        for col in range(24, 27):
            matrix.SetPixel(row, col, *red)
    for row in range(11, 14):
        for col in range(27, 30):
            matrix.SetPixel(row, col, *blue)

   # ShutDown
    for row in range(22, 24):  
        for col in range(17, 23):
            matrix.SetPixel(row, col, *red)
    for row in range(21, 25):   
        for col in range(27, 29):
            matrix.SetPixel(row, col, *red)
    for row in range(19, 21):  
        for col in range(25, 27):
            matrix.SetPixel(row, col, *red)
    for row in range(25, 27):   
        for col in range(25, 27):
            matrix.SetPixel(row, col, *red)
    for row in range(17, 19):   
        for col in range(21, 25):
            matrix.SetPixel(row, col, *red)
    for row in range(27, 29):   
        for col in range(21, 25):
            matrix.SetPixel(row, col, *red)
    for row in range(19, 21):   
        for col in range(19, 21):
            matrix.SetPixel(row, col, *red)
    for row in range(25, 27):   
        for col in range(19, 21):
            matrix.SetPixel(row, col, *red)


# Funktion zum Zeichnen des Bildschirms
def draw_screen(x, y):
    # Farbe der Linien
    color = (255, 255, 255) #weiß
    red = (255, 0, 0)
    blue = (0, 0, 255)
    orange = (255, 165, 0)

    # Zeichnen der vertikalen Linie
    for row in range(32):
        matrix.SetPixel(0, row, *color)
        matrix.SetPixel(15, row, *color)
        matrix.SetPixel(31, row, *color)

    # Zeichnen der horizontalen Linie
    for col in range(32):
        matrix.SetPixel(col, 0, *color)
        matrix.SetPixel(col, 15, *color)
        matrix.SetPixel(col, 31, *color)

    # Zeichne die Piktogramme
    draw_pictograms()

    # Zeichne das orange Quadrat basierend auf der Position
    x_pos = int(x * 15)
    y_pos = int(y * 15)

    for i in range(16):
        matrix.SetPixel(i + x_pos, y_pos, *orange)
        matrix.SetPixel(x_pos, i + y_pos, *orange)
        matrix.SetPixel(i + x_pos, 15 + y_pos, *orange)
        matrix.SetPixel(15 + x_pos, i + y_pos, *orange)

# Funktion zur Spieleauswahl
def select_game():
    draw_screen(orange_square_position[0], orange_square_position[1])

def run_game():
    # Überprüfen, ob bereits eine Instanz von tictactoe läuft
    for proc in psutil.process_iter():
        if "tictactoe.py" in proc.cmdline():
            proc.kill()  # Beende die vorherige Instanz

    # Starte eine neue Instanz von tictactoe
    subprocess.call("sudo python tictactoe.py", shell=True)

def game_finished():
    select_game()   # Zurück zur Spieleauswahl

def main():
    global orange_square_position
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    running = True
    while running:
        clear_screen()
        select_game()  # Zeichne den Bildschirm für die Spieleauswahl
        orange_square_position = [0, 0]  # Setze die Position des orangen Quadrats zurück

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                # Bewegung des Joysticks verarbeiten
                if event.axis == 0:  # Horizontal
                    if event.value > 0:
                        orange_square_position[0] = min(1, orange_square_position[0] + 1)
                    elif event.value < 0:
                        orange_square_position[0] = max(0, orange_square_position[0] - 1)
                elif event.axis == 1:  # Vertikal
                    if event.value > 0:
                        orange_square_position[1] = min(1, orange_square_position[1] + 1)
                    elif event.value < 0:
                        orange_square_position[1] = max(0, orange_square_position[1] - 1)
            elif event.type == pygame.JOYBUTTONDOWN:
                # Tastendruck des Joysticks verarbeiten
                if event.button == 1:  # Annahme, dass Button 1 die Auswahl bestätigt
                    if orange_square_position == [0, 0]:
                        print("Colorbattle wurde ausgewählt")
                    elif orange_square_position == [1, 0]:
                        run_game()
                        game_finished()
                    elif orange_square_position == [0, 1]:
                        print("VierGewinnt wurde ausgewählt")
                    elif orange_square_position == [1, 1]:
                        print("ShutDown wurde ausgewählt")
                        subprocess.call("sudo shutdown -h now", shell=True)

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
