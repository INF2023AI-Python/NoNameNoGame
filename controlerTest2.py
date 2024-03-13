import pygame
from pygame.locals import *

def main():
    # Initialisieren von Pygame
    pygame.init()
    
    # Einrichten des Bildschirms
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Gamepad Test')
    
    # Initialisieren des Gamepads
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("Kein Gamepad gefunden.")
        return
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Gamepad gefunden:", joystick.get_name())
    
    # Hauptereignisschleife
    running = True
    while running:
        # Ereignisse verarbeiten
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == JOYAXISMOTION:
                if joystick.get_axis(0) > 0.9:
                    print("left")
                elif joystick.get_axis(0) == -1:
                    print("right")
                if joystick.get_axis(1) > 0.9:
                    print("up")
                elif joystick.get_axis(1) == -1:
                    print("down")
            elif event.type == JOYBUTTONDOWN:
                print("Taste {} gedrückt".format(event.button))
            elif event.type == JOYBUTTONUP:
                print("Taste {} losgelassen".format(event.button))
            elif event.type == JOYHATMOTION:
                print("Hut {}: {}".format(event.hat, event.value))
    
    # Aufräumen
    pygame.quit()

if __name__ == '__main__':
    main()
