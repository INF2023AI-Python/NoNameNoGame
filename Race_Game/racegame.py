import pygame
import time
import math
import os
from utils import scale_image
from utils import blit_rotate_center

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Kein Gamepad gefunden.")

joystick = pygame.joystick.Joystick(0)     
joystick.init()
print("Gamepad gefunden:"), joystick.get_name()

# Pfad
python_file_path = os.path.abspath(__file__)
python_file_directory = os.path.dirname(python_file_path)
os.chdir(python_file_directory)

# Laden der Bilder
GRASS = pygame.image.load("Graphics/green_background.png")
TRACK = scale_image(pygame.image.load("Graphics/racetrack.png"), 0.9)
TRACK_BOARDER = scale_image(pygame.image.load("Graphics/boarder.png"), 0.9)
TRACK_BOARDER_MASK = pygame.mask.from_surface(TRACK_BOARDER)
FINISH = pygame.image.load("Graphics/finish.png")
FINISH_POSITION = (0, -52)

# Autos
RED_CAR = scale_image(pygame.image.load("Graphics/car_red.png"), 0.04)

MAX_SPEED = 4
MAX_ROTATION = 6
pygame.mixer.init()
ENGINE_SOUND = pygame.mixer.Sound("Sounds/car_sound.mp3")
CRASH_SOUND = pygame.mixer.Sound("Sounds/crash_sound.mp3")

start_cooldown = 0.5
sound_playing = False
collision_cooldown = 2.0  # Zeit in Sekunden für den Cooldown nach Kollision
last_collision_time = 0.0  # Zeitstempel der letzten Kollision

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Racing Game")

FPS = 60

class AbstractCar:
    IMG = RED_CAR

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.3

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (350, 450)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.sound_playing = False
        self.max_sound_volume = 0.1
        self.min_sound_volume = 0
        self.volume_range = self.max_sound_volume - self.min_sound_volume
       
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        global last_collision_time
        if time.time() - last_collision_time > collision_cooldown:
            CRASH_SOUND.play()
            last_collision_time = time.time()
        self.vel = -self.vel
        self.move()

    def sound_car(self):
        global sound_playing
        if self.vel != 0 and not self.sound_playing:
            ENGINE_SOUND.play(-1)
            self.sound_playing = True
        elif self.vel == 0 and self.sound_playing:
            pass
        volume_factor = self.vel / self.max_vel
        volume = self.min_sound_volume + volume_factor * self.volume_range
        ENGINE_SOUND.set_volume(volume)

def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BOARDER, (0, 0))]
player_car = PlayerCar(MAX_SPEED, MAX_ROTATION)

while run:
    clock.tick(FPS)

    elapsed_time = 0

    # Ereignisschleife
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                player_car.reset()
        
    # Steuerung des Autos
    if joystick.get_axis(0) > 0.9:
        player_car.rotate(right=True)
    elif joystick.get_axis(0) == -1:
        player_car.rotate(left=True)
        
    if joystick.get_button(1):
        moved = True
        player_car.move_forward()
        
    if joystick.get_button(2):
        moved = True
        player_car.move_backward()

    if joystick.get_button(3):
        player_car.reset()

    if joystick.get_button(0):
        pygame.quit()
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()
        moved = False

    # Kollision mit der Streckenbegrenzung
    if player_car.collide(TRACK_BOARDER_MASK) is not None:
        player_car.bounce()      
    
    # Zeichnen des Bildschirms
    draw(WIN, images, player_car)
    player_car.sound_car()

