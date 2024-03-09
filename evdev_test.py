from evdev import InputDevice, categorize, ecodes

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for device in devices:

   print(device.path, device.name, device.phys)
