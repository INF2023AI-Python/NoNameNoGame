import pygame
import random

pygame.init()
windowWidth = 1024
windowHeight = 600
screen= pygame.display.set_mode((windowWidth, windowHeight))
clock= pygame.time.Clock()
running= True

#variables
rows = 5
collumns =5
alienCooldown= 1000
lastAlienShot = pygame.time.get_ticks()
spaceshipSize = 60
numberHealth = 3


#colors
black= (0,0,0)
red = (255,0,0)
green= (0,255,0)

#background
sideWidth = (windowWidth - windowHeight) // 2
centerImage = pygame.image.load('Space Invaders/png/bg.png')
imageHeight = windowHeight
centerImage = pygame.transform.scale(centerImage, (imageHeight, imageHeight))


#spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Space Invaders/png/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.lastShot = pygame.time.get_ticks()
        self.healthStart = health
        self.healthRemaining = health

    def update(self):
        speed = 8
        shootingSpeed = 500
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > sideWidth:
            self.rect.x -=speed
        if key[pygame.K_RIGHT] and self.rect.right < (windowWidth-sideWidth):
            self.rect.x +=speed
        #shoot
        timeNow = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and timeNow - self.lastShot > shootingSpeed:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.lastShot = timeNow
        #mask
        self.mask = pygame.mask.from_surface(self.image)
        #health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), (self.rect.width - 13), 15))
        if self.healthRemaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 5), int((self.rect.width - 13)*(self.healthRemaining / self.healthStart)), 15))
            



#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Space Invaders/png/bullet.png')
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
        self.image = pygame.image.load("Space Invaders/png/alien"+ str(random.randint(1,4))+ ".png")
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
        self.image = pygame.image.load('Space Invaders/png/alien_bullet.png')
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
            alien = Aliens(sideWidth+ 105 + item * 100, 50+row * 60)
            alien.image = pygame.transform.scale(alien.image, (35, 35)) 
            alien_group.add(alien)
create_aliens()





spaceship = Spaceship(int (windowWidth /2), windowHeight-70, numberHealth)
spaceship.image= pygame.transform.scale(spaceship.image,(spaceshipSize,spaceshipSize))
spaceship_group.add(spaceship)


while running:

    screen.fill((0,0,0))
    pygame.draw.rect(screen, black, (0, 0, sideWidth, windowHeight)) 
    pygame.draw.rect(screen, black, (windowWidth - sideWidth, 0, sideWidth, windowHeight)) 
    screen.blit(centerImage, ((windowWidth - imageHeight) // 2, (windowHeight - imageHeight) // 2))
    

    timeNow = pygame.time.get_ticks()
    if timeNow - lastAlienShot > alienCooldown and len(alien_bullet_group) < 5 and len(alien_group) > 0:
        shootingAlien = random.choice(alien_group.sprites())
        alienBullet = AlienBullets(shootingAlien.rect.centerx, shootingAlien.rect.bottom)
        alien_bullet_group.add(alienBullet)
        lastAlienShot = timeNow
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    spaceship.update()

    bullet_group.update()
    alien_group.update()
    alien_bullet_group.update()

    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit