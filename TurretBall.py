from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0/0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class TurretBall:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        if TurretBall.image == None:
            TurretBall.image = load_image('Monster/turret/turret_ball.png')
        self.x, self.y, self.velocity, self.dir = x, y, RUN_SPEED_PPS, dir
        self.sizeX, self.sizeY = 60, 60
        self.damage = 10


    def get_bb(self):
        if self.dir < 2:
            return self.x - 20, self.y - 40, self.x + 20, self.y + 40
        else:
            return self.x - 35, self.y - 20, self.x + 35, self.y + 20

    def draw(self):
        self.image.clip_draw(self.dir * self.sizeX, 0, self.sizeX, self.sizeY, int(self.x), int(self.y))
        draw_rectangle(*self.get_bb())


    def update(self):
        if self.dir == 0 :
            self.y += self.velocity * game_framework.frame_time
        elif self.dir == 1:
            self.y -= self.velocity * game_framework.frame_time
        elif self.dir == 2 :
            self.x -= self.velocity * game_framework.frame_time
        elif self.dir == 3:
            self.x += self.velocity * game_framework.frame_time

        if self.x < 150 or self.x > 1130 or self.y < 100 or self.y > 635:
            game_world.remove_object(self)

