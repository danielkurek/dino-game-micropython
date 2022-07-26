
from machine import Pin, SPI
import ssd1306
import time
from game_engine import *

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

#display init
spi = SPI(1, 80_000_000, sck=Pin(10), mosi=Pin(11))
display_width = 128
display_height = 64
display = ssd1306.SSD1306_SPI(display_width, display_height, spi, dc=Pin(8), res=Pin(7), cs=Pin(9))

# load images
dino_path = "/images/dino-cropped-20-22.pbm"
cactus_path = "/images/cactus.pbm"

dino = Image(dino_path)
cactus = Image(cactus_path)

player = MovingObject(10, display_height - dino.height, dino, display)
obstacle = MovingObject(50, display_height - cactus.height, cactus, display)

now = time.ticks_ms()
player.physics_tick(now)
player.set_pos(10, display_height - dino.height)
obstacle.physics_tick(now)
obstacle.set_pos(120, display_height - cactus.height)

objects = [player, obstacle]

obstacle.set_motion_vector(-1.5,0)

while True:
    display.fill(0)
    now = time.ticks_ms()
    if button_up.value() == 1 and player.on_ground():
        player.set_motion_vector(0,-3.5)
    if obstacle.x <= -cactus.width:
        obstacle.set_pos(x=128)
    for o in objects:
        o.physics_tick(now)
    for o in objects:
        o.draw()
    display.show()
    

# collision_group = [obstacle]

# def game_loop():
#     while True:
#         if button_up.value() == 1:
#             player.jump()
#         player.physics_tick()
#         obstacle.physics_tick()
#         collision = player.collision_test(collision_group)
#         if collision != None:
#             return False
#         display.fill(0)
#         player.draw(display)
#         obstacle.draw(display)
#         display.show()
#         time.sleep_ms(10)

# display.text("Press ACT", 27, 25)
# display.show()


# while True:
#     if button_action.value() == 1:
#         player = Player(dino, dino_w, dino_h, 10, display_height - dino_h, display_width, display_height)
#         game_loop()
#         display.text("Press ACT", 27, 25)
#         display.show()
