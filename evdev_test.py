import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions

sys.path.append("/home/pi/.local/lib/python3.9/site-packages")

from evdev import InputDevice, categorize, ecodes

dev = InputDevice('/dev/input/event4')

print(dev)

for event in dev.read_loop():

    if event.type == ecodes.EV_KEY:

        print(categorize(event))
