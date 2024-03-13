import pygame
from pygame.locals import *

pygame.init()

joystick = pygame.joystick.Joystick(0)

while True:
    for event in pygame.event.get(): # get the events (update the joystick)
        if event.type == QUIT: # allow to click on the X button to close the window
            pygame.quit()
            exit()

    if joystick.get_button(0):
        print("X")
    elif joystick.get_button(1):
        print("A")
    elif joystick.get_button(2):
        print("B")
    elif joystick.get_button(3):
        print("Y")
    elif joystick.get_button(4):
        print("left")
    elif joystick.get_button(5):
        print("right")
    elif joystick.get_button(8):
        print("SELECT")
    elif joystick.get_button(9):
        print("START")  
    elif joystick.get_axis(0):
        if joystick.get_axis(0) == 1:
            print("up")
        elif joystick.get_axis(0) == -1:
            print("right")
    elif joystick.get_axis(1):
        print("TEST")
