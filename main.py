import pygame
import os
import sys
from pygame.locals import *

pygame.init()
windowWidth = 1024
windowHeight = 600
screen= pygame.display.set_mode((windowWidth, windowHeight)) # pygame.FULLSCREEN
running= True

#path
#python_file_path = os.path.abspath(__file__)
#python_file_directory = os.path.dirname(python_file_path)
#os.chdir(python_file_directory)

#fonds
font = pygame.font.SysFont('Constantia', 30)


#colors
black= (0,0,0)
red = (255,0,0)
green= (0,255,0)
white= (255,255,255)
blue= (0,0,255)
gray= (200,200,200)

# Initialisieren des Gamepads
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

current_directory = os.path.dirname(__file__)

def program1():
    os.system(sys.executable + " " + os.path.join(current_directory, "Race_Game", "racegame.py"))

def program2():
    os.system(sys.executable + " " + os.path.join(current_directory, "Space_Invaders", "Spaceinvaders.py"))

def program3():
    os.system(sys.executable + " " + os.path.join(current_directory, "frogger" "frogger.py"))

def program4():
    os.system(sys.executable + " " + os.path.join(current_directory, "frogger" "frogger.py"))


# Schaltflächen
button_width, button_height = 200, 50
button_padding = 20

buttons = []
button_texts = ["Programm 1", "Programm 2", "Programm 3", "Programm 4"]
button_functions = [program1, program2, program3, program4]
selected_button = 0

for i, text in enumerate(button_texts):
    button_x = (windowWidth - button_width) // 2
    button_y = 150 + i * (button_height + button_padding)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    buttons.append((button_rect, text, button_functions[i]))



while running:

    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == JOYAXISMOTION:
            axis = event.axis
            value = event.value
            if axis == 1 and abs(value) > 0.5:
                if value < 0:
                    selected_button = (selected_button + 1) % len(buttons)
                elif value > 0:
                    selected_button = (selected_button - 1) % len(buttons) 
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 3 :
             buttons[selected_button][2]()
            
        
    screen.fill(black)  
            
    text = font.render("Hauptmenü", True, white)
    text_rect = text.get_rect(center=(windowWidth // 2, 100))
    screen.blit(text, text_rect)

    for i, button in enumerate(buttons):
        if i == selected_button:
            pygame.draw.rect(screen, blue, button[0])
        else:
            pygame.draw.rect(screen, gray, button[0])
        text = font.render(button[1], True, white)
        text_rect = text.get_rect(center=button[0].center)
        screen.blit(text, text_rect)
    
       


    pygame.display.flip()
pygame.quit