# Fun-with-Friends

## Set-up
+ Hardware: 2 gamepads, Adafruit RGB Matrix + Real Time Clock HAT 32x32
+ Choose Storage e.g. 32 GB SD-Card
1. Install Raspberry Pi OS using Raspberry Pi Imager
  + https://www.raspberrypi.com/software/
  + Choose Raspberry Pi OS with desktop and recommended software for 32-Bit if you use Raspberry Pi 3
+ Afer first boot
  + connect to wifi using 
  ```
  sudo raspi-config
  ``` 
    or by the gui
  + get the newest updates using 
  ```
  sudo apt update
  ```
2. Install Adafruit RGB Matrix + Real Time Clock HAT for Raspberry Pi
  + https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi
  ```
  curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-
  Scripts/main/rgb-matrix.sh >rgb-matrix.sh
  sudo bash rgb-matrix.sh
  ```
  + Questions will be asked. If you have the same hardware as us, the response would be as follows:
    + CONTINUE? -y
    + Select interface board type: -2 (Adafruit RGB Matrix HAT + RTC)
    + What is thy bidding? -1 (Quality (disables sound, requires solderin))
    + A reboot is required after installation.

  + add `isolcpus=3` at the end in the `/boot/cmdline.text`

3. Install Python3
  ```
  sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
  make build-python PYTHON=$(command -v python3)
  sudo make install-python PYTHON=$(command -v python3)
  ```
4. Install Fun-with-Friends Repo
  ```
  git clone https://github.com/INF2023AI-Python/Fun-with-Friends.git
  ```
5. Set-up for Autostart
  + give startbildschrim.py execution rights
      ```
    chmod +x / /home/pi/Fun-with-Friends/startbildschirm.py
      ```
  + Extend autostart file
      ```
      sudo nano /etc/rc.local
      ```
    + Add the following text before "exit 0"
      ```
       python3  /home/pi/Fun-with-Friends/startbildschirm.py &
      ```
  + finish with rebooting
  ```
   sudo reboot
  ```

## Game description
### Start Screen
Use the arrow keys to move the orange square.
Select a game or power off by pressing the red 'A' key.

### Snake
Snake is a game where the player manoeuvres a 'snake' around the board. The objective is to maximize the size of the snake before the game ends.  The snake grows in size by consuming food and the game ends when the  snake collides with itself or when the time limit of 60 seconds is reached.  

How to Play:
+ Use the arrow keys to move the snake around.

### TicTacToe
Two players compete in a 3x3 grid. They take turns placing crosses or circles. The first player to create a straight row of three symbols, either horizontally, vertically, or diagonally, wins the game.

How to Play:
+ Use the arrow keys to move the orange square.
+ Select your symbol's position by pressing the red 'A' key.
+ Player X will begin.

### VierGewinnt
The objective of 'Vier Gewinnt' is to strategically place four pieces of your own colour in a row, either diagonally, horizontally, or vertically. The first player to achieve this is declared the winner.

How to Play:
+ Use the arrow keys to move your colour. 
+ Select your column by pressing the red 'A' key.
+ Player 1 is assigned the colour red.
+ Player 2 is shown in blue.

### Color Battle
Two players attempt to fill in as much space as possible with their respective colours within a 60-second time limit.

How to Play:
+ Use the arrow keys to move your colour.