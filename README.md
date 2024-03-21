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
  + add `isolcpus=3` at the end in the `/boot/cmdline.text`
  + `sudo reboot`
+ Install Python3
  + https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
+ Install Fun-with-Friends Repo
  + https://github.com/INF2023AI-Python/Fun-with-Friends.git
+ Set-up für Autostart
  + startbildschrim.py Ausführungsrechte geben
    + `chmod +x / /home/pi/Fun-with-Friends/startbildschirm.py`
  + Autostartdatei erweitern
    + `sudo nano /etc/rc.local`
    + vor "exit 0" folgenden Text ergänzen
      + `python3  /home/pi/Fun-with-Friends/startbildschirm.py &`
  + `sudo reboot`

## Game description
### Start Screen
Use the arrow keys to move the orange square.
Select a game or power off by pressing the red 'A' key.

### TBA

### TicTacToe
Two players compete in a 3x3 grid. They take turns placing crosses or circles. The first player to create a straight row of three symbols, either horizontally, vertically, or diagonally, wins the game.

How to Play:
Use the arrow keys to move the orange square.
Select your symbol's position by pressing the red 'A' key.
Player X will begin.

### VierGewinnt
The objective of 'Vier Gewinnt' is to strategically place four pieces of your own colour in a row, either diagonally, horizontally, or vertically. The first player to achieve this is declared the winner.

How to Play:
Use the arrow keys to move your colour. 
Select your column by pressing the red 'A' key.
Player 1 is assigned the colour red.
Player 2 is shown in blue.