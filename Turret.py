from pico2d import *
import game_framework
import random

MAP_WIDTH, MAP_HEIGHT = 1270, 717

TIME_OUT = range(2)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:
    def enter(Turret, event):
        pass
    def exit(Turret, event):
        pass

    def do(Turret):
        if abs(Turret.Dx - Turret.x) > abs(Turret.Dy - Turret.y):
            if Turret.Dx > Turret.x:
                Turret.direction = 3
            else:
                Turret.direction = 2
        else:
            if Turret.Dy > Turret.y:
                Turret.direction = 0
            else:
                Turret.direction = 1

        Turret.frame = (Turret.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        Turret.x = clamp(150, Turret.x, 1130)
        Turret.y = clamp(100, Turret.y, 635)

    def draw(Turret):
        Turret.sizex = 60
        Turret.sizey = 90
        Turret.image = load_image('Monster/Turret/turret.png')
        Turret.image.clip_draw(int(Turret.frame) * Turret.sizex, 0, Turret.sizex, Turret.sizey, int(Turret.x), int(Turret.y))

class AttackState:
    def enter(Turret, event):
        pass

    def exit(Turret, event):
        pass

    def do(Turret):
        if abs(Turret.Dx - Turret.x) > abs(Turret.Dy - Turret.y):
            if Turret.Dx > Turret.x:
                Turret.direction = 3
            else:
                Turret.direction = 2
        else:
            if Turret.Dy > Turret.y:
                Turret.direction = 0
            else:
                Turret.direction = 1

        Turret.frame = (Turret.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if int(Turret.frame) == 7 :
            Turret.add_event(TIME_OUT)



    def draw(Turret):
        Turret.sizex = 60
        Turret.sizey = 90
        Turret.image = load_image('Monster/Turret/turret.png')
        Turret.image.clip_draw(int(Turret.frame) * Turret.sizex, 0, Turret.sizex, Turret.sizey, int(Turret.x), int(Turret.y))

next_state_table = {
    IdleState: {TIME_OUT: AttackState},
    AttackState: {TIME_OUT: IdleState},

}

class Turret():
    def __init__(self):
        self.image = load_image('Monster/Turret/turret.png')

        self.frame = 0
        self.direction = 3

        self.x, self.y = random.randint(150, 1130), random.randint(100, 635)
        #주인공의 좌표 값을 받기 위한 변수
        self.Dx, self.Dy = self.x, self.y
        self.t = 0
        self.font=load_font('ENCR10B.TTF',16)


        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        self.sizex = 100
        self.sizey = 80

        self.hp = 100

    def get_bb(self):
        if self.cur_state==IdleState:
            return self.x - (self.sizex//2-10), self.y - (self.sizey//2-20), self.x + (self.sizex//2-10), self.y + (self.sizey//2-20)
        elif self.cur_state==AttackState:
            return self.x - (self.sizex//2-10), self.y - 50 , self.x + (self.sizex//2-10), self.y + 50

    def hited(self, damage):
        self.hp -= damage
        if self.direction == 3:
            self.x -= 5
        elif self.direction == 2:
            self.x += 5
        elif self.direction == 0:
            self.y -= 5
        elif self.direction == 1:
            self.y += 5

    def change_state(self, state):
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_event(self, event):
        pass

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 30, self.y + 65, 'HP: %d' % self.hp, (255, 255, 0))
        draw_rectangle(*self.get_bb())

