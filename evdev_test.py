import sys

sys.path.append("/home/pi/.local/lib/python3.9/site-packages")

import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:

   print(device.path, device.name, device.phys)
