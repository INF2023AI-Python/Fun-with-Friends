import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import subprocess
import psutil

orange_square_position = [0, 0]
game_running = False

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

def run_game():
    global game_running
    # Überprüfen, ob bereits eine Instanz von tictactoe läuft
    for proc in psutil.process_iter():
        if "tictactoe.py" in proc.cmdline():
            proc.kill()  # Beende die vorherige Instanz

    # Starte eine neue Instanz von tictactoe
    subprocess.call("sudo python tictactoe.py", shell=True)
    game_running = True

# Funktion zum Zeichnen des Hauptbildschirms
def draw_main_screen():
    # Farben definieren
    color = (255, 255, 255)  # weiß
    orange = (255, 165, 0)  # orange
    red = (255, 0, 0)  # rot
    blue = (0, 0, 255)  # blau

    # Vertikale Linien zeichnen
    for row in range(32):
        matrix.SetPixel(0, row, *color)
        matrix.SetPixel(15, row, *color)
        matrix.SetPixel(31, row, *color)

    # Horizontale Linien zeichnen
    for col in range(32):
        matrix.SetPixel(col, 0, *color)
        matrix.SetPixel(col, 15, *color)
        matrix.SetPixel(col, 31, *color)

    # Zeichnen der orangefarbenen Linien für die Optionen
    for i in range(16):
        matrix.SetPixel(i, 0, *orange)
        matrix.SetPixel(15 + i, 0, *orange)
        matrix.SetPixel(i, 15, *orange)
        matrix.SetPixel(15 + i, 15, *orange)

    # Zeichnen der Piktogramme für die Optionen
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

# Funktion zum Zeichnen des Bildschirms während des Spiels
def draw_game_screen():
    # Hier müssten Sie die Zeichenlogik für den Spielbildschirm implementieren
    pass

def select_option(new_position):
    global game_running
    if new_position[0] == 0 and new_position[1] == 0:
        print("Colorbattle wurde ausgewählt")
    elif new_position[0] == 1 and new_position[1] == 0:       
        run_game()
        print("Tictactoe wurde ausgewählt")
    elif new_position[0] == 0 and new_position[1] == 1:
        print("VierGewinnt wurde ausgewählt")
    elif new_position[0] == 1 and new_position[1] == 1:
        print("ShutDown wurde ausgewählt")
        subprocess.call("sudo shutdown -h now", shell=True)

def update_orange_square_position(orange_square_position, joystick):
    # Erhalte die Achsenpositionen des Joysticks
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Bewegungsrichtung basierend auf den Achsenwerten mit Toleranz
    if -0.2 < x_axis < 0.2 and y_axis < -0.8:
        # Bewege nach oben
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] - 1))]
        print("Bewege nach oben")
    elif -0.2 < x_axis < 0.2 and y_axis > 0.8:
        # Bewege nach unten
        new_position = [max(0, min(1, orange_square_position[0])),
                        max(0, min(1, orange_square_position[1] + 1))]
        print("Bewege nach unten")
    elif x_axis > 0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach rechts
        new_position = [max(0, min(1, orange_square_position[0] + 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Bewege nach rechts")
    elif x_axis < -0.8 and -0.2 < y_axis < 0.2:
        # Bewege nach links
        new_position = [max(0, min(1, orange_square_position[0] - 1)),
                        max(0, min(1, orange_square_position[1]))]
        print("Bewege nach links")
    else:
        # Keine Bewegung, wenn keine der Bedingungen erfüllt ist
        new_position = orange_square_position

    # Überprüfe, ob der Button mit der ID 1 gedrückt wurde
    if joystick.get_button(1) == 1:
        select_option(new_position)

    # Rückgabe der neuen Position
    return new_position

def main():
    global orange_square_position, game_running
    # Pygame und Controllerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick aus
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    running = True
    while running:
        clear_screen()
        if not game_running:
            draw_main_screen()
        else:
            draw_game_screen()

        # Rufe update_orange_square_position auf, um die Position des orangen Quadrats zu aktualisieren
        orange_square_position = update_orange_square_position(orange_square_position, joystick)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    main()
