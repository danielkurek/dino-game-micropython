import framebuf
import time

from image_lib import read_image

# TODO: move coordinate origin to bottom left corner (0,64)
# TODO: collision detection

class Image():
    def __init__(self, path):
        self.bitmap, self.width, self.height = read_image(path)

class Sprite():
    def __init__(self, x, y, image, display):
        self.set_pos(x, y)
        self.image = image
        self.display = display
    
    
    def change_image(self, image):
        self.image = image
    
    def draw(self):
        if self.image != None:
            self.display.blit(self.image.bitmap, int(self.x), int(self.y), framebuf.MONO_VLSB)
    
    def set_pos(self, x = None, y = None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y


class MovingObject(Sprite):
    def __init__(self, x, y, image, display, ground = 64, gravity = 0.15):
        super().__init__(x, y, image, display)
        self.motion_vector = [0, 0]
        self.gravity = gravity
        self.ground = ground
        self.last_tick = 0
    
    def set_motion_vector(self, x, y):
        if x != None:
            self.motion_vector[0] = x
        if y != None:
            self.motion_vector[1] = y

    def physics_tick(self, now):
        diff = time.ticks_diff(now, self.last_tick)

        self.motion_vector[1] += self.gravity * diff * 0.1

        self.x = self.x + self.motion_vector[0] * diff * 0.1
        self.y = self.y + self.motion_vector[1] * diff * 0.1

        if self.gravity != 0 and self.y >= self.ground - self.image.height:
            self.y = self.ground - self.image.height
            self.motion_vector[1] = 0

        self.last_tick = now

    def on_ground(self):
        return self.y == self.ground - self.image.height
    
    def collision_test(self, obstacles):
        for obstacle in obstacles:
            if (self.x + self.image.width >= obstacle.x and obstacle.x + obstacle.image.width >= self.x and
                self.y + self.image.height >= obstacle.y and obstacle.y + obstacle.image.height >= self.y):
                return obstacle
        return None

def stop_objects(objects):
    for o in objects:
        o.set_motion_vector(0,0)
