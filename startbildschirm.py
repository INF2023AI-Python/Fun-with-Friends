import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import subprocess
import psutil

# Konstanten für die Bildschirmmodi
MODE_MENU = 0
MODE_GAME = 1

# Initialer Modus
current_mode = MODE_MENU

# Orange Quadrat Position
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

# Funktion zum Starten des Spiels
def run_game():
    global current_mode
    subprocess.call("sudo python tictactoe.py", shell=True)
    current_mode = MODE_MENU  # Zurück zum Menümodus nach Spielende

# Funktion zum Zeichnen des Bildschirms im Menü-Modus
def draw_menu_screen():
    global orange_square_position
    # Zeichne das Menü hier...
    draw_screen()

# Funktion zum Zeichnen des Bildschirms im Spielmodus
def draw_game_screen():
    # Zeichne das Spiel hier...
    draw_screen()
    
# Funktion zum Überprüfen des Modus und Zeichnen des entsprechenden Bildschirms
def draw_screen():
    if current_mode == MODE_MENU:
        draw_menu_screen()
    elif current_mode == MODE_GAME:
        draw_game_screen()

# Funktion zum Auswählen einer Option im Menü
def select_option(new_position):
    if new_position[0] == 0 and new_position[1] == 0:
        print("Colorbattle wurde ausgewählt")
    elif new_position[0] == 1 and new_position[1] == 0:       
        global current_mode
        current_mode = MODE_GAME
        run_game()
    elif new_position[0] == 0 and new_position[1] == 1:
        print("VierGewinnt wurde ausgewählt")
    elif new_position[0] == 1 and new_position[1] == 1:
        print("ShutDown wurde ausgewählt")
        subprocess.call("sudo shutdown -h now", shell=True)

# Funktion zum Aktualisieren der Position des orangefarbenen Quadrats
def update_orange_square_position(joystick):
    # Logik zur Aktualisierung der Position des orangefarbenen Quadrats hier...
    return [0, 0]  # Dummy-Rückgabewert

def main():
    # Pygame und Controllerprüfung
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Joystick gefunden.")
        pygame.quit()
        quit()

    # Wähle den ersten verfügbaren Joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    running = True
    while running:
        clear_screen()
        
        # Zeichne den aktuellen Bildschirm basierend auf dem aktuellen Modus
        draw_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Wenn im Menümodus, aktualisiere die Position des orangefarbenen Quadrats
        if current_mode == MODE_MENU:
            global orange_square_position
            orange_square_position = update_orange_square_position(joystick)
            # Überprüfe, ob eine Option ausgewählt wurde
            if joystick.get_button(0):
                select_option(orange_square_position)

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
