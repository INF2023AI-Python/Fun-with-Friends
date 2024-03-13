import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import subprocess
import psutil

orange_square_position = [0, 0]
game_running = False  # Variable, um den Status des Tic Tac Toe-Spiels zu verfolgen

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
    if not game_running:
        # Überprüfen, ob bereits eine Instanz von tictactoe läuft
        for proc in psutil.process_iter():
            if "tictactoe.py" in proc.cmdline():
                proc.kill()  # Beende die vorherige Instanz

        # Starte eine neue Instanz von tictactoe
        subprocess.call("sudo python tictactoe.py", shell=True)
        game_running = True

# Funktion zum Zeichnen des Bildschirms
def draw_screen(x, y):
    # Dein Code zum Zeichnen des Bildschirms hier ...

def select_option(new_position):
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
    # Dein Code zum Aktualisieren der orangen Quadratposition hier ...


def main():
    global orange_square_position, game_running
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
        # Rufe update_orange_square_position auf, um die Position des orangen Quadrats zu aktualisieren
        orange_square_position = update_orange_square_position(orange_square_position, joystick)
        # Übergebe die aktualisierte Position an draw_screen
        draw_screen(orange_square_position[0], orange_square_position[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
