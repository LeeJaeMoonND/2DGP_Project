from pico2d import *
import random
import classMan

MAP_WIDTH, MAP_HEIGHT = 1175, 585

# Random한 좌표를 지나는 몬스터
class RMon():
    def __init__(self):
        self.image = load_image('mon2.png')
        self.frame = 0
        self.direction = 2
        self.p1 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p2 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p3 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.p4 = [random.randint(100, MAP_WIDTH-100), random.randint(100, MAP_HEIGHT-100)]
        self.x, self.y = self.p2[0], self.p2[1]
        self.t = 0

    def draw(self):
        self.image.clip_draw(self.frame*94, self.direction*93, 94, 93, self.x, self.y)

    def move(self):
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

        self.frame = (self.frame + 1) % 5
        self.t += 0.01
        if self.t >= 1.0:
            self.p1, self.p2, self.p3, self.p4 = self.p2, self.p3, self.p4, [random.randint(0, 800), random.randint(0, 600)]
            self.t = 0

#추적하는 몬스터
class TMon():
    def __init__(self):
        self.image = load_image('mon1.png')
        self.frame = 0
        self.direction = 8
        self.x, self.y = random.randint(0, 800), random.randint(0, 600)
        self.t = 0

    def draw(self):
        self.image.clip_draw(self.frame*67, self.direction*68, 67, 68, self.x, self.y)

    def move(self, Tx, Ty):
        self.t = (1000-abs(Tx-self.x))/50000
        self.x = (self.t * Tx) + (1-self.t) * self.x

        self.y = (self.t * Ty) + (1-self.t) * self.y

        self.frame = (self.frame + 1) % 5
