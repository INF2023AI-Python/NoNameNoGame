# NoNameNoGame

## Set-up
+ Hardware: Raspberry Pi 5, Dispay 1023x600, Joystick and 6 Buttons
+ Choose Storage e.g. 32 GB SD-Card

![console](https://github.com/INF2023AI-Python/NoNameNoGame/assets/158037983/2a140b00-0486-47b8-b097-e428eeb822d8)

### Install Python3

 > https://www.python.org/downloads/

### Install NoNameNoGame
  ```
  git clone https://github.com/INF2023AI-Python/NoNameNoGame.git
  ```
### Set-up for Autostart
+ Make sure the file is executeable
  ```
  chmod +x /path/to/main.py
  ```
  
+ Edit the "rc.local" file
  
  ```
  sudo nano /etc/rc.local
  ```

+ Add the following command to the "rc.local" file
  ```
  python3 /home/pi/main.py &
  ```

## Game description
### Start Screen
Use the Joystick to select the game 
Press the green button to start the game

### Racing Game

Small racing game to improve your own racing skills. Race against the clock and beat your time or that of your friend. In the future, the previous lap and the fastest lap will also be displayed and who knows, several tracks offer even more opportunities to improve. <br>
How to Play:
+ Use the joystick to move the car left or right
+ Press the green button to move forward
+ Press the blue button next to the green button to move backward
+ Press the top blue button to reset the car


### Space Invaders

Shoot some Aliens with your little Spaceship and try not to get shot yourself. <br>
How to Play:
+ Use the Joystick to move the space ship around
+ It is like you would expect it - left=left, right=right
+ Press the Green Button to shoot

### Frogger

Cross the street without touching the cars and use the logs to cross the water. <br>
How to Play:
+ Use the Joystick to move the rectangle around
+ It is like you would expect it - top = up, bottom = down, left=left, right=right



### Chess
PvP Chess Game without en passant, castling and pawn promotion

How to Play: <br>
+ Use the Joystick to move the rectangle around
+ It is like you would expect it - top = up, bottom = down, left=left, right=right
+ Use the Green Button to select a piece an the destination
+ Use the Red Button to exit the game


