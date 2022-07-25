
from machine import Pin, SPI
import framebuf
import ssd1306
import utime
import random
import time

from image_lib import read_image

piezo = Pin(9, Pin.OUT)

button_0 = Pin(0, Pin.IN, Pin.PULL_DOWN)
button_1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
button_2 = Pin(2, Pin.IN, Pin.PULL_DOWN)
button_3 = Pin(3, Pin.IN, Pin.PULL_DOWN)
button_4 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button_5 = Pin(5, Pin.IN, Pin.PULL_DOWN)

button_up = button_0
button_down = button_1
button_left = button_2
button_right = button_3
button_back = button_4
button_action = button_5

# games status codes
GAME_READY = 0
GAME_PLAY = 1
GAME_OVER = 2

#display init
spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))
display_width = 128
display_height = 64
display = ssd1306.SSD1306_SPI(display_width, display_height, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))

# load images
dino_path = "/images/dino-cropped-20-22.pbm"
cactus_path = "/images/cactus.pbm"

dino, dino_w, dino_h = read_image(dino_path, 1)
cactus, cactus_w, cactus_h = read_image(cactus_path, 1)


display.blit(dino, 0, display_height - dino_h, 0)
display.blit(cactus, dino_w, display_height - cactus_h, 0)
display.blit(cactus, dino_w * 3, display_height - cactus_h, 0)
display.show()

class Player():
    RUNNING = 0
    JUMPING = 1
    def __init__(self, image, w, h, x, y, display_w, display_h, jump_force = -4):
        self.image = image
        self.w = w
        self.h = h
        self.display_w = display_w
        self.display_h = display_h
        self.x = x
        self.y = y
        self.state = Player.RUNNING
        self.gravity = 0.2
        self.jump_force = jump_force
        self.moving_vector = [0,0]
        self.ground = y


    def draw(self, display):
        display.blit(self.image, int(self.x), int(self.y), 0)
    
    def jump(self):
        if self.state == Player.RUNNING:
            self.state = Player.JUMPING
            self.moving_vector[0] = 0
            self.moving_vector[1] = self.jump_force
    
    def collision_test(self, obstacles):
        for obstacle in obstacles:
            if (self.x + self.w >= obstacle.x and obstacle.x + obstacle.w >= self.x and
                self.y + self.h >= obstacle.y and obstacle.y + obstacle.h >= self.y):
                return obstacle
        return None
    
    def physics_tick(self):
        if self.state == Player.JUMPING:
            self.moving_vector[1] += self.gravity
            self.x = self.x + self.moving_vector[0]
            self.y = self.y + self.moving_vector[1]

            if self.y >= self.ground:
                self.state = Player.RUNNING
                self.y = self.ground
                self.moving_vector[1] = 0

class Cactus():
    def __init__(self, image, w, h, x, y, display_w, display_h, speed=1.5):
        self.image = image
        self.w = w
        self.h = h
        self.display_w = display_w
        self.display_h = display_h
        self.x = x
        self.y = y
        self.state = Player.RUNNING
        self.moving_vector = [-speed,0]
        self.speed = speed


    def draw(self, display):
        display.blit(self.image, int(self.x), int(self.y), 0)
    
    def physics_tick(self):
        self.x = self.x + self.moving_vector[0]

        if self.x <= 0:
            self.x = display_width


player = Player(dino, dino_w, dino_h, 10, display_height - dino_h, display_width, display_height)
obstacle = Cactus(cactus, cactus_w, cactus_h, display_width, display_height - cactus_h, display_width, display_height)

collision_group = [obstacle]

def game_loop():
    while True:
        if button_up.value() == 1:
            player.jump()
        player.physics_tick()
        obstacle.physics_tick()
        collision = player.collision_test(collision_group)
        if collision != None:
            return False
        display.fill(0)
        player.draw(display)
        obstacle.draw(display)
        display.show()
        time.sleep_ms(10)

display.text("Press ACT", 27, 25)
display.show()


while True:
    if button_action.value() == 1:
        player = Player(dino, dino_w, dino_h, 10, display_height - dino_h, display_width, display_height)
        game_loop()
        display.text("Press ACT", 27, 25)
        display.show()
