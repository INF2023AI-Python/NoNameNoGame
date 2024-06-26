import pygame
from pygame.locals import *
import random
import os
import sys
import time

pygame.init()
windowWidth = 1024
windowHeight = 600
screen= pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN) # pygame.FULLSCREEN
clock= pygame.time.Clock()
running= True


#path
python_file_path = os.path.abspath(__file__)
python_file_directory = os.path.dirname(python_file_path)
os.chdir(python_file_directory)

#variables
rows = 4
collumns =9
alienCooldown= 1000
lastAlienShot = pygame.time.get_ticks()
spaceshipSize = 60
numberHealth = 3
countdown = 3
lastCount = pygame.time.get_ticks()
gameOver = 0
gameOverTime = pygame.time.get_ticks()
gameOverTimeSet = 0
endMenu = 0


#fonds
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

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



#background
centerImage = pygame.image.load('png/bg.png')
imageHeight = windowHeight
centerImage = pygame.transform.scale(centerImage, (windowWidth,windowHeight))

#text
def draw_text(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

def restart():
    
    
    global numberHealth, gameOver, gameOverTimeSet, countdown
    numberHealth = 3
    gameOver = 0
    gameOverTimeSet = 0
    countdown = 4
    spaceship_position = (int (windowWidth /2), windowHeight-70)
    spaceship.image= pygame.transform.scale(spaceship.image,(spaceshipSize,spaceshipSize))
    spaceship_group.add(spaceship)
    destroyBullets()  # Zerstört vorhandene Projektile
    clearScreen()  # Entfernt vorhandene Aliens
    create_aliens()  # Erstellt neue Aliens
    spaceship.healthRemaining = numberHealth  # Setzt die Lebenspunkte des Raumschiffs zurück
    spaceship.rect.center = spaceship_position  # Stellt die Position des Raumschiffs wieder her
    spaceship_group.add(spaceship)
  
def mainMenu():
    pygame.quit()


#spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('png/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.lastShot = pygame.time.get_ticks()
        self.healthStart = health
        self.healthRemaining = health

    def update(self):
        speed = 8
        gameOver = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 1:
            self.rect.x -=speed
        if key[pygame.K_RIGHT] and self.rect.right < windowWidth:
            self.rect.x +=speed
        if joystick.get_axis(0) > 0.9 and self.rect.left > 1:
            self.rect.x -=speed
        elif joystick.get_axis(0) == -1 and self.rect.right < windowWidth:
            self.rect.x +=speed
        #shoot
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                
        #mask
        self.mask = pygame.mask.from_surface(self.image)

        #health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), (self.rect.width - 13), 15))
        if self.healthRemaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 5), int((self.rect.width - 13)*(self.healthRemaining / self.healthStart)), 15))
        elif self.healthRemaining <= 0:
            self.kill()
            gameOver = -1
            pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), (self.rect.width - 13), 15))
        return gameOver
            



#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('png/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill() 
            

#aliens
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("png/alien"+ str(random.randint(1,4))+ ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('png/alien_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        self.rect.y += 2
        if self.rect.top > windowHeight:
            self.kill()
        if pygame.sprite.spritecollide(self,spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.healthRemaining -= 1
    


#groups
spaceship_group= pygame.sprite.Group()
bullet_group= pygame.sprite.Group()
alien_group= pygame.sprite.Group()
alien_bullet_group= pygame.sprite.Group()


def create_aliens():
    for row in range(rows):
        for item in range(collumns):
            alien = Aliens(115 + item * 100, 70+row * 70)
            alien.image = pygame.transform.scale(alien.image, (35, 35)) 
            alien_group.add(alien)
create_aliens()



def destroyBullets():
    bullet_group.empty()
    alien_bullet_group.empty()


def clearScreen():
    alien_group.empty()
    spaceship_group.empty()


spaceship = Spaceship(int (windowWidth /2), windowHeight-70, numberHealth)
spaceship.image= pygame.transform.scale(spaceship.image,(spaceshipSize,spaceshipSize))
spaceship_group.add(spaceship)


button_width, button_height = 300, 70
button_padding = 20

buttons = []
button_texts = ["Play again", "Main menu"]
button_functions = [restart, mainMenu]
selected_button = 0


for i, text in enumerate(button_texts):
    button_x = (windowWidth - button_width) // 2
    button_y = 200 + i * (button_height + button_padding)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    buttons.append((button_rect, text, button_functions[i]))


def endScreen():
    clearScreen()
    screen.fill(black)
    for i, button in enumerate(buttons):
        if i == selected_button:
            pygame.draw.rect(screen, blue, button[0])
        else:
            pygame.draw.rect(screen, gray, button[0])
        text = font30.render(button[1], True, white)
        text_rect = text.get_rect(center=button[0].center)
        screen.blit(text, text_rect)


while running:

    
    
    screen.blit(centerImage, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 3 and countdown == 0 and gameOver == 0:
            bullet = Bullets(spaceship.rect.centerx, spaceship.rect.top)
            bullet_group.add(bullet)
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
             mainMenu()
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 1:
             restart()
        elif event.type == JOYAXISMOTION:
                axis = event.axis
                value = event.value
                if axis == 1 and abs(value) > 0.5:
                    if value < 0:
                        selected_button = (selected_button + 1) % len(buttons)
                    elif value > 0:
                        selected_button = (selected_button - 1) % len(buttons) 
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 3 :
                if endMenu == 1:
                    buttons[selected_button][2]()
            

    if countdown == 0:

        timeNow = pygame.time.get_ticks()
        if timeNow - lastAlienShot > alienCooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0 and gameOver == 0:
            shootingAlien = random.choice(alien_group.sprites())
            alienBullet = AlienBullets(shootingAlien.rect.centerx, shootingAlien.rect.bottom)
            alien_bullet_group.add(alienBullet)
            lastAlienShot = timeNow

        if len(alien_group) == 0:
            gameOver = 1
        
        if gameOver == 0:
            gameOver = spaceship.update()
            bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
        else: 
            if gameOver == -1:
                draw_text('GAME OVER!', font40, white, int(windowWidth / 2 - 100 ), int(windowHeight / 2 + 50))
                destroyBullets()
            if gameOver == 1:
                draw_text('YOU WIN!', font40, white, int(windowWidth / 2 - 100 ), int(windowHeight / 2))
                destroyBullets()
                clearScreen()
            if gameOverTimeSet == 0:
                gameOverTime = pygame.time.get_ticks()
                gameOverTimeSet = 1
                selected_button = 0
            elif pygame.time.get_ticks() - gameOverTime > 5000:
                endScreen()  
                endMenu = 1

            
            
               

    if countdown > 0:
        draw_text('SPACE INVADERS', font40, white, int(windowWidth / 2 - 150 ), int(windowHeight / 2 + 50))
        draw_text(str(countdown), font40, white, int(windowWidth / 2 - 10 ), int(windowHeight / 2 + 100))
        countTimer = pygame.time.get_ticks()
        if countTimer - lastCount > 1000:
            countdown -= 1
            lastCount =countTimer

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)



    
       


    pygame.display.flip()
    clock.tick(60)
pygame.quit