import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Initialisiere den Joystick
pygame.joystick.init()

# Überprüfe, ob ein Joystick angeschlossen ist
if pygame.joystick.get_count() == 0:
    print("Kein Joystick gefunden.")
    sys.exit()

# Hole den ersten Joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Gebe Informationen zum Joystick aus
print(f"Joystick-Name: {joystick.get_name()}")
print(f"Anzahl der Achsen: {joystick.get_numaxes()}")
print(f"Anzahl der Tasten: {joystick.get_numbuttons()}")

# Hauptschleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Bewegung der Joystick-Achse
            achse = event.axis
            wert = event.value
            print(f"Achse {achse}: {wert:.2f}")
        elif event.type == pygame.JOYBUTTONDOWN:
            # Tastendruck am Joystick
            taste = event.button
            print(f"Taste {taste} gedrückt")
        elif event.type == pygame.JOYBUTTONUP:
            # Tastenfreigabe am Joystick
            taste = event.button
            print(f"Taste {taste} losgelassen")
        elif event.type == pygame.QUIT:
            # Beende das Programm
            pygame.quit()
            sys.exit()
