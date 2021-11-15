from pico2d import *
import random
import classMan

MAP_WIDTH, MAP_HEIGHT = 1270, 717


# Random한 좌표를 지나는 몬스터
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
        self.image.clip_draw(self.frame*50, self.direction*50, 50, 50, self.x, self.y)

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

class IdleState:
    def enter(TMon, event):
        pass

    def exit(TMon, event):
        pass

    def do(TMon):
        pass

    def draw(TMon):
        TMon.image = load_image('Monster/Golem/_Golem-idle.png')


class TMon():
    def __init__(self):
        self.image = load_image('Monster/Golem/golem-attack1.png')
        self.frame = 0
        self.direction = 3
        self.x, self.y = random.randint(0, 800), random.randint(0, 600)
        self.t = 0
        self.sizex = 100
        self.sizey = 80

    def draw(self):
        self.image.clip_draw(self.sizex *self.frame, 0 *self.sizey, self.sizex, self.sizey, self.x, self.y)

    def move(self, Tx, Ty):
        if abs(Tx-self.x)>abs(Ty-self.y):
            if Tx > self.x :
                self.direction = 3
                self.image = load_image('Monster/Golem/_Golem-idle.png')
                self.sizex = 70
                self.sizey = 110
            else :
                self.direction = 2
                self.image = load_image('Monster/Golem/golem-attack1.png')
                self.sizex = 100
                self.sizey = 80
        else :
            if Ty > self.y:
                self.direction = 0
            else:
                self.direction = 1

        self.t = (1000-abs(Tx-self.x))/50000

        self.x = (self.t * Tx) + (1-self.t) * self.x

        self.y = (self.t * Ty) + (1-self.t) * self.y

        self.frame = (self.frame + 1) % 8
