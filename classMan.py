from pico2d import *
import random

MAP_WIDTH, MAP_HEIGHT = 1175, 585

class Man():
    def __init__(self):
        self.image = load_image('will animation cycle35.35.png')
        self.frame = 0
        # 움직임
        self.dir = 0
        self.direction=0

        # 좌표, 방향
        self.dirX = 0
        self.dirY = 0
        self.p = (self.x, self.y) = (MAP_WIDTH / 2, MAP_HEIGHT / 2)

        # 상태 체크
        self.isRoll = False
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
            self.dirX += 1
            self.direction = 3
        elif n == 'ML':
            self.isMove = 1
            self.dirX -= 1
            self.direction = 2

        elif n == 'MU':
            self.isMove = 1
            self.dirY += 1
            self.direction = 0
        elif n == 'MD':
            self.isMove = 1
            self.dirY -= 1
            self.direction = 1
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

    def rolling(self):
        self.isRoll = True
        self.frame = 0
        self.speed = 3

    def attack(self):
        self.is_attack = True
        self.isMove=True
        # 시트를 바꾸면 새로 짤 예정
        self.frame = 0

    def location(self):
        self.frame = (self.frame + 1) % 8
        if self.frame == 7 and self.is_attack == True:
            self.is_attack = False
            self.isMove = False
        if self.frame == 7 and self.isRoll == True :
            self.isRoll = False
            self.speed = 1

        self.x += self.dirX *5 * self.speed
        self.y += self.dirY *5 * self.speed


        if self.x < 125 :
            self.x = 125
        elif MAP_WIDTH-100<self.x :
            self.x = MAP_WIDTH-100
        if self.y < 150:
            self.y = 150
        elif MAP_HEIGHT+50<self.y:
            self.y = MAP_HEIGHT+50

    def draw(self):

        if self.isMove == True:
            self.image = load_image('will animation cycle35.35.png')
        else:
            self.image = load_image('Will_Idle35.35.png')
        if self.isRoll == True:
            self.image = load_image('Will_Roll35.35.png')
        if self.is_attack == True:
            self.image = load_image('attack.png')
        self.image.clip_draw(self.frame*70, self.direction*70, 70, 70, self.x, self.y)
