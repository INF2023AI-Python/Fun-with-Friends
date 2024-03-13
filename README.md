# Fun-with-Friends

## Set-up
+ Hardware: 2 gamepads, Adafruit RGB Matrix + Real Time Clock HAT 32x32
+ Choose Storage e.g. 32 GB SD-Card
+ Install Raspberry Pi OS
  + https://www.raspberrypi.com/software/
  + Raspberry Pi OS with desktop and recommended software for 32-Bit if you use Raspberry Pi 3
+ Install Adafruit RGB Matrix + Real Time Clock HAT for Raspberry Pi
  + https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi
  + choose Quality binding
  + add 'isolcpus=3' at the end in the /boot/cmdline.text, then reboot
+ Install Python3
  + https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
+ Install Fun-with-Friends Repo
  + https://github.com/INF2023AI-Python/Fun-with-Friends.git
+ Set-up für Autostart
  + Führe folgende Befehler aus
  + sudo nano /etc/xdg/lxsession/LXDE-pi/autostart (open the autostart file)
  + @sudo python3 /path/to/your/startbildschirm.py (at this to the end of the fil)
  + sudo reboot
