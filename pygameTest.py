import pygame
import sys

pygame.init()
screen = pygame.display.set_mode([1920,1080])
background = pygame.image.load("Graphics/background.jpg")
clock = pygame.time.Clock()
pygame.display.set_caption("NoName - NoGame")

def draw():
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (255,255,0), (x,y, width,high))
    pygame.display.update()

x = 300
y = 300
speed = 3
width = 40
high = 80

lBoarder = pygame.draw.rect(screen, (0,0,0), (-2,0,2,600), 0)
rBoarder =

go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        y -= speed
    if pressed[pygame.K_RIGHT]:
        x += speed
    if pressed[pygame.K_DOWN]:
        y += speed
    if pressed[pygame.K_LEFT]:
        x -= speed

    draw()
    pygame.display.flip()  # Fenster aktualisieren
    clock.tick(60)
