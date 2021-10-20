from pico2d import *
import random

MAP_WIDTH, MAP_HEIGHT = 1175, 585

class Man():
    def __init__(self):
        self.image = load_image('man.png')
        self.frame = 0
        self.dir = 0
        self.direction=0
        self.p = (self.x, self.y) = (MAP_WIDTH/2,MAP_HEIGHT/2)
        self.dirX = 0
        self.dirY = 0
        self.isMove = False
        self.is_attack = False

        # 아직 생각만 하고 있는 능력치
        self.hp = 100
        self.mp = 100
        self.speed = 1
        self.damage = 5


    def move(self, n):
        if n == 'MR':
            self.isMove = 1
            self.dirX += self.speed
            self.direction = 0
        elif n == 'ML':
            self.isMove = 1
            self.dirX -= self.speed
            self.direction = 1
        elif n == 'MU':
            self.isMove = 1
            self.dirY += self.speed
        elif n == 'MD':
            self.isMove = 1
            self.dirY -= self.speed
        elif n == 'SR':
            self.isMove = 0
            self.dirX -= 1
        elif n == 'SL':
            self.isMove = 0
            self.dirX += self.speed
        elif n == 'SU':
            self.isMove = 0
            self.dirY -= self.speed
        elif n == 'SD':
            self.isMove = 0
            self.dirY += self.speed

    def attack(self):
        self.is_attack = True
        self.isMove=True
        if self.direction == 1 :
            #시트를 바꾸면 새로 짤 예정
            self.dir = 1
            self.frame = 0
            self.direction = 2
        elif self.direction == 0 :
            self.dir = 0
            self.frame = 0
            self.direction = 3

    def location(self):
        if(self.isMove == True):
            self.frame = (self.frame + 1) % 8
        else :
            self.frame = 7
        if self.frame == 7 and self.is_attack == True:
            self.is_attack = False
            self.isMove = False
            if self.dir == 0:
                self.direction = 0
            elif self.dir == 1:
                self.direction = 1
        self.x += self.dirX*5
        self.y += self.dirY*5

    def draw(self):
        self.image.clip_draw(self.frame*160, self.direction*109, 160, 109, self.x, self.y)
