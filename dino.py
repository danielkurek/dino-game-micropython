
from machine import Pin, SPI
import ssd1306
import time
from game_engine import *
import random

# file access
import io

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

best_score_path = "/best_score.txt"

# load images
dino_path = "/images/dino-cropped-20-22.pbm"
cactus_path = "/images/cactus.pbm"

dino_img = Image(dino_path)
cactus_img = Image(cactus_path)

player = MovingObject(10, display_height - dino_img.height, dino_img, display)
cactus = MovingObject(50, display_height - cactus_img.height, cactus_img, display)

now = time.ticks_ms()
player.physics_tick(now)
player.set_pos(10, display_height - dino_img.height)
cactus.physics_tick(now)
cactus.set_pos(120, display_height - cactus_img.height)

objects = [player, cactus]
obstacles = [cactus]

cactus.set_motion_vector(-1.5,0)

def game_loop():
    global score

    now = time.ticks_ms()
    # update time in physics loop
    player.physics_tick(now)
    cactus.physics_tick(now)

    # reset position
    player.set_pos(10, display_height - dino_img.height)
    cactus.set_pos(120, display_height - cactus_img.height)

    score = 0

    while True:
        display.fill(0)
        now = time.ticks_ms()
        if button_up.value() == 1 and player.on_ground():
            player.set_motion_vector(0,-3.5)
        if cactus.x <= -cactus_img.width :
            cactus.set_pos(x=128 + random.randint(0, 128))
            score += 1 # original game counts score as a distance travelled
        for o in objects:
            o.physics_tick(now)
        for o in objects:
            o.draw()
        display.text(str(score), 64, 0)
        display.show()
        if player.collision_test(obstacles) != None:
            break

def start_text():
    display.text("Press ACT", 25, 20, 1)
    display.text("Best: " + str(best_score), 32, 10, 1)
    display.show()

best_score = 0

try:
    with io.open(best_score_path, "r") as f:
        try:
            best_score = int(f.readline())
        except ValueError:
            print("cannot read best score")
except OSError:
    print("file not found")
    

start_text()

while True:
    if button_action.value() == 1:
        game_loop()
        if score != None and score > best_score:
            # add animation or other indication of new best score
            best_score = score
            with io.open(best_score_path, "w") as f:
                f.write(str(score))
        start_text()
    

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
