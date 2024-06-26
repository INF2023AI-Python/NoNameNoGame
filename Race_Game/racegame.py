import pygame
import time
import math
import os
from utils import scale_image
from utils import blit_rotate_center

#Initalization pygame, joystick and Sound
pygame.init()
pygame.joystick.init()
pygame.mixer.init()

if pygame.joystick.get_count() == 0:
    print("Kein Gamepad gefunden.")

joystick = pygame.joystick.Joystick(0)     
joystick.init()
print("Gamepad gefunden:"), joystick.get_name()

# Pfad
python_file_path = os.path.abspath(__file__)
python_file_directory = os.path.dirname(python_file_path)
os.chdir(python_file_directory)

#fonds
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#Loading pictures
FLAG = pygame.image.load("Graphics/racingflag.png")
GRASS = pygame.image.load("Graphics/green_background.png")
TRACK = scale_image(pygame.image.load("Graphics/racetrack.png"), 0.9)
TRACK_BOARDER = scale_image(pygame.image.load("Graphics/boarder.png"), 0.9)
TRACK_BOARDER_MASK = pygame.mask.from_surface(TRACK_BOARDER)
FINISH = pygame.image.load("Graphics/finish.png")
FINISH_POSITION = (620, 410)
STARTBOX1 = pygame.image.load("Graphics/startposition.png")
STARTBOX1_POSITION = (580, 428)
STARTBOX2 = pygame.image.load("Graphics/startposition.png")
STARTBOX2_POSITION = (550, 475)

#car
RED_CAR = scale_image(pygame.image.load("Graphics/car_red.png"), 0.04)

#loading sounds
ENGINE_SOUND = pygame.mixer.Sound("Sounds/car_sound.mp3")
CRASH_SOUND = pygame.mixer.Sound("Sounds/crash_sound.mp3")

#Constants
MAX_SPEED = 4
MAX_ROTATION = 6
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
collision_cooldown = 2.0  
last_collision_time = 0.0  
sound_playing = False
FPS = 60

#Set up screen and caption
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Racing Game")


class AbstractCar: #for all cars, necessary for multiplayer, etc.
    IMG = RED_CAR

    def __init__(self, max_vel, rotation_vel): #Initalization of the different variables
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = -90
        self.x, self.y = self.START_POS
        self.acceleration = 0.3

    def rotate(self, left=False, right=False):  #Rotation car
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):    #draw car
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self): #forward
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self): #backward
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self): #mathematical calculation for movement
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):  #collide
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self): #reset
        self.x, self.y = self.START_POS
        self.angle = -90
        self.vel = 0

class PlayerCar(AbstractCar): #only for the red car
    IMG = RED_CAR
    START_POS = (549, 416)

    def __init__(self, max_vel, rotation_vel): #Initalization of variables
        super().__init__(max_vel, rotation_vel)
        self.sound_playing = False
        self.max_sound_volume = 0.1
        self.min_sound_volume = 0
        self.volume_range = self.max_sound_volume - self.min_sound_volume
        self.finished = False
        self.start_time = 0
        self.end_time = 0

    def reduce_speed(self): #Reduce speed
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self): #bounce from boarder
        global last_collision_time
        if time.time() - last_collision_time > collision_cooldown:
            CRASH_SOUND.play()
            last_collision_time = time.time()
        self.vel = -self.vel
        self.move()

    def sound_car(self): #carsound
        global sound_playing
        if self.vel != 0 and not self.sound_playing:
            ENGINE_SOUND.play(-1)
            self.sound_playing = True
        elif self.vel == 0 and self.sound_playing:
            pass
        volume_factor = self.vel / self.max_vel
        volume = self.min_sound_volume + volume_factor * self.volume_range
        ENGINE_SOUND.set_volume(volume)

def draw(win, images, player_car, lap_time): #draw function for images and car
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    
    #Rendering Text + Background
    lap_text_surface = font30.render("Rundenzeit: {:.2f}s".format(lap_time), True, (255, 255, 255))
    lap_background_surface = pygame.Surface((lap_text_surface.get_width(), lap_text_surface.get_height()))
    lap_background_surface.fill((200,200,200))
    lap_background_surface.blit(lap_text_surface, (0, 0))
    
    #Position text
    lap_rect = lap_background_surface.get_rect(center=(WIDTH // 2, 20))
    
    #draw text
    win.blit(lap_background_surface, lap_rect)
    pygame.display.update()

#variables
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION),(STARTBOX1, STARTBOX1_POSITION),(STARTBOX1, STARTBOX2_POSITION), (TRACK_BOARDER, (0, 0))]
player_car = PlayerCar(MAX_SPEED, MAX_ROTATION)
lap_start_time = 0
lap_started = False  
first_lap_started = False  #Variable to determine whether the first round has started
round_cooldown = False

countdown = 3  #Initalization countdown start

#loop
while run:
    clock.tick(FPS)

    elapsed_time = 0

    #Eventloop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                player_car.reset()
        
    #loading screen   
    if countdown > 0:
        WIN.blit(FLAG, (0,0)) 
        countdown_surface = font40.render("RACEGAME", True, (255, 255, 255))
        countdown_rect = countdown_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(countdown_surface, countdown_rect)
        pygame.display.update()
        time.sleep(1)  
        countdown -= 1  
        continue  
        
    #Steering the car only after countdown
    #control with joystick

    if joystick.get_axis(0) < -0.9:#right
        player_car.rotate(right=True)
    elif joystick.get_axis(0) > 0.9:#left
        player_car.rotate(left=True)
        
    if joystick.get_button(3):#forward
        moved = True
        player_car.move_forward()
        
    if joystick.get_button(4):#backward
        moved = True
        player_car.move_backward()

    if joystick.get_button(1):#reset
        player_car.reset()

    if joystick.get_button(0):#quit
        pygame.quit()
    
    keys = pygame.key.get_pressed()
    moved = False

    #control with keyboard
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

    
    #collision with boarder
    if player_car.collide(TRACK_BOARDER_MASK) is not None:
        player_car.bounce()

    #logic for timekeeping
    if player_car.collide(pygame.mask.from_surface(FINISH), FINISH_POSITION[0], FINISH_POSITION[1]):
        if not player_car.finished:
            player_car.finished = True
            player_car.end_time = time.time()
            lap_time = player_car.end_time - lap_start_time
            print("Rundenzeit:", lap_time)
            lap_start_time = time.time()
        else:
            player_car.finished = False
            player_car.start_time = time.time()


    if player_car.collide(pygame.mask.from_surface(FINISH), FINISH_POSITION[0], FINISH_POSITION[1]) and not lap_started:
        lap_start_time = time.time()
        lap_started = True
        first_lap_started = True  


    if first_lap_started:  
        draw(WIN, images, player_car, time.time() - lap_start_time)
    else:
        draw(WIN, images, player_car, 0)  

    player_car.sound_car()

    #only for testing necessary
    #print("X-Koordinate:", player_car.x)
    #print("Y-Koordinate:", player_car.y)
pygame.quit()
