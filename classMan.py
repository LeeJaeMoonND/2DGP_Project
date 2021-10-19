from pico2d import *
import random

MAP_WIDTH, MAP_HEIGHT = 1175, 585

class Man():
    def __init__(self):
        self.image = load_image('man.png')
        self.frame = 0
        self.direction=0
        self.p = (self.x, self.y) = (MAP_WIDTH/2,MAP_HEIGHT/2)
        self.isMove = 0
        self.dirX = 0
        self.dirY = 0

    def move(self, n):
        if n == 'MR':
            self.isMove = 1
            self.dirX += 1
            self.direction = 0
        elif n == 'ML':
            self.isMove = 1
            self.dirX -= 1
            self.direction = 2
        elif n == 'MU':
            self.isMove = 1
            self.dirY += 1
            self.direction = 1
        elif n == 'MD':
            self.isMove = 1
            self.dirY -= 1
            self.direction = 3

        elif n == 'SR':
            self.isMove = 0
            self.dirX -= 1
        elif n == 'SL':
            self.isMove = 0
            self.dirX += 1
        elif n == 'SU':
            self.isMove = 0
            self.dirY -= 1
        elif n == 'SD':
            self.isMove = 0
            self.dirY += 1

    def location(self):
        if self.isMove == 1:
            self.frame = (self.frame + 1) % 7
        self.x += self.dirX*5
        self.y += self.dirY*5

    def draw(self):
        self.image.clip_draw(self.frame*120, self.direction*130, 120, 130, self.x, self.y)
