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

GRASS = pygame.image.load("Graphics/green_background.png")
TRACK = scale_image(pygame.image.load("Graphics/racetrack.png"), 0.9)

TRACK_BOARDER = scale_image(pygame.image.load("Graphics/boarder.png"), 0.9)
TRACK_BOARDER_MASK = pygame.mask.from_surface(TRACK_BOARDER)
FINISH = pygame.image.load("Graphics/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (0, -52)

RED_CAR = scale_image(pygame.image.load("Graphics/car_red.png"), 0.04)
GREEN_CAR = pygame.image.load("Graphics/car_green.png")

pygame.mixer.init()
ENGINE_SOUND = pygame.mixer.Sound("Sounds/car_sound.mp3")
CRASH_SOUND = pygame.mixer.Sound("Sounds/crash_sound.mp3")

sound_playing = False

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
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
        self.max_sound_volume = 0.2
        self.min_sound_volume = 0
        self.volume_range = self.max_sound_volume - self.min_sound_volume
        self.crossed_start_line = False
        self.timer_started = False
        self.start_time = 0
        self.elapsed_time = 0
        #self.highscore_file = "highscore.txt"
        #self.highscore = self.load_highscore()
        self.previous_time = 0

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()
        CRASH_SOUND.play()

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

    def load_highscore(self):
        if os.path.exists(self.highscore_file):
            with open(self.highscore_file, 'r') as f:
                try:
                    return float(f.read())
                except ValueError:
                    return 0
        else:
            return 0

    def save_highscore(self, score):
        with open(self.highscore_file, 'w') as f:
            f.write(str(score))

def draw(win, images, player_car, elapsed_time, highscore, previous_time):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    font = pygame.font.Font(None, 36)
    text_time = font.render("Elapsed Time: {:.2f} Sekunden".format(elapsed_time), True, (255, 255, 255))
    text_highscore = font.render("Highscore: {:.2f} Sekunden".format(highscore), True, (255, 255, 255))
    text_previous_time = font.render("Previous Time: {:.2f} Sekunden".format(previous_time), True, (255, 255, 255))
    win.blit(text_time, (10, 10))
    win.blit(text_highscore, (10, 50))
    win.blit(text_previous_time, (10, 90))
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BOARDER, (0, 0))]
player_car = PlayerCar(8, 8)

while run:
    clock.tick(FPS)

    elapsed_time = 0
    if player_car.timer_started:
        player_car.previous_time = player_car.elapsed_time
        elapsed_time = time.time() - player_car.start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
        elif event.type == JOYAXISMOTION:
            if joystick.get_axis(0) > 0.9:
                print("left")
                player_car.rotate(left=True)
            elif joystick.get_axis(0) == -1:
                print("right")
                player_car.rotate(right=True)
            if joystick.get_axis(1) > 0.9:
                print("up")
                moved = True
                player_car.move_forward()
            elif joystick.get_axis(1) == -1:
                print("down")
                moved = True
                player_car.move_backward()
        
        if event.type == pygame.KEYDOWN:
            if joystick.get_button(0):
                player_car.reset()
                player_car.crossed_start_line = False
                player_car.timer_started = False
                player_car.start_time = 0
                player_car.elapsed_time = 0
                player_car.highscore = player_car.load_highscore()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                player_car.reset()
                player_car.crossed_start_line = False
                player_car.timer_started = False
                player_car.start_time = 0
                player_car.elapsed_time = 0
                player_car.highscore = player_car.load_highscore()

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

    if player_car.collide(TRACK_BOARDER_MASK) is not None:
        player_car.bounce()

    if player_car.x < 545:
        player_car.crossed_start_line = False

    if 545 <= player_car.x <= 570 and 350 <= player_car.y <= 500:
        if not player_car.crossed_start_line:
            player_car.crossed_start_line = True
            player_car.timer_started = True
            player_car.start_time = time.time()
        elif player_car.crossed_start_line and player_car.x > 570:
            player_car.previous_time = player_car.elapsed_time
            print(player_car.previous_time)
            player_car.timer_started = False
            player_car.elapsed_time = time.time() - player_car.start_time
            #if player_car.previous_time < player_car.highscore or player_car.highscore == 0:
                #player_car.highscore = player_car.previous_time
                #player_car.save_highscore(player_car.highscore)  # Highscore speichern

    draw(WIN, images, player_car, elapsed_time, player_car.highscore, player_car.previous_time)
    player_car.sound_car()

pygame.quit()
