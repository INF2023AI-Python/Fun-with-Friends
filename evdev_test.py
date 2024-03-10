import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

sys.path.append("/home/pi/.local/lib/python3.9/site-packages")

#from evdev import InputDevice, categorize, ecodes

#dev = InputDevice('/dev/input/event4')

#print(dev)

#for event in dev.read_loop():

   # if event.type == ecodes.EV_KEY:

      #  print(categorize(event))


import evdev

options = RGBMatrixOptions()
options.cols = 32
options.rows = 32
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options=options)

# Finde den Pfad des Controllers
controller_path = None
for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
    if "gamepad" in device.name.lower():
        controller_path = device.path
        break

if controller_path is None:
    print("Kein Controller gefunden.")
else:
    print("Controller gefunden:", controller_path)

# Öffne den Controller
controller = evdev.InputDevice(controller_path)

target_button = 288

def handle_key_event(event):
    if event.type == evdev.ecodes.EV_KEY and event.code == target_button:
        matrix.SetPixel(10, 10, 255, 0, 0)

# Hauptprogramm
for event in controller.read_loop():
    handle_key_event(event)
