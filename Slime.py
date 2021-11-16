from pico2d import *
import game_framework
import random

MAP_WIDTH, MAP_HEIGHT = 1270, 717

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class RMon():
    def __init__(self):
        self.image = load_image('Monster/slime/slime.png')
        self.frame = 0
        self.direction = 0
        self.p1 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p2 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p3 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p4 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.x, self.y = self.p2[0], self.p2[1]
        self.t = 0

    def draw(self):
        self.image.clip_draw(int(self.frame)*50, self.direction*50, 50, 50, self.x, self.y)

    def update(self):
        self.x = ((-self.t**3 + 2*self.t**2 - self.t)*self.p1[0] + (
                3*self.t**3 - 5*self.t**2 + 2)*self.p2[0] + (
                -3*self.t**3 + 4*self.t**2 + self.t)*self.p3[0] + (self.t**3 - self.t**2)*self.p4[0])/2

        self.y = ((-self.t**3 + 2*self.t**2 - self.t)*self.p1[1] + (
                3*self.t**3 - 5*self.t**2 + 2)*self.p2[1] + (
                -3*self.t**3 + 4*self.t**2 + self.t)*self.p3[1] + (self.t**3 - self.t**2)*self.p4[1])/2
        if self.x > MAP_WIDTH-100:
            self.x = MAP_WIDTH-100
        elif self.x < 100:
            self.x = 100
        if self.y > MAP_HEIGHT-100:
            self.y = MAP_HEIGHT-100
        elif self.y < 100:
            self.y = 100

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        self.t += 0.01
        if self.t >= 1.0:
            self.p1, self.p2, self.p3, self.p4 = self.p2, self.p3, self.p4, [random.randint(0, 800), random.randint(0, 600)]
            self.t = 0