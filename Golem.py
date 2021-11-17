from pico2d import *
import game_framework
import random

MAP_WIDTH, MAP_HEIGHT = 1270, 717

CONTACT, UNCONTACT= range(2)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class IdleState:
    def enter(Golem, event):
        pass
    def exit(Golem, event):
        pass

    def do(Golem):
        if abs(Golem.Dx - Golem.x) > abs(Golem.Dy - Golem.y):
            if Golem.Dx > Golem.x:
                Golem.direction = 3
            else:
                Golem.direction = 2
        else:
            if Golem.Dy > Golem.y:
                Golem.direction = 0
            else:
                Golem.direction = 1

        Golem.t = 0.01
        Golem.x = (Golem.t * Golem.Dx) + (1 - Golem.t) * Golem.x
        Golem.y = (Golem.t * Golem.Dy) + (1 - Golem.t) * Golem.y
        Golem.frame = (Golem.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Golem.x = clamp(150, Golem.x, 1130)
        Golem.y = clamp(100, Golem.y, 635)




    def draw(Golem):
        Golem.sizex = 70
        Golem.sizey = 110
        Golem.image = load_image('Monster/Golem/_Golem-idle.png')
        Golem.image.clip_draw(int(Golem.frame) * Golem.sizex, Golem.direction * Golem.sizey, Golem.sizex, Golem.sizey, int(Golem.x), int(Golem.y))

class AttackState:
    def enter(Golem, event):
        pass

    def exit(Golem, event):
        pass

    def do(Golem):
        if abs(Golem.Dx - Golem.x) > abs(Golem.Dy - Golem.y):
            if Golem.Dx > Golem.x:
                Golem.direction = 3
            else:
                Golem.direction = 2
        else:
            if Golem.Dy > Golem.y:
                Golem.direction = 0
            else:
                Golem.direction = 1

        Golem.frame = (Golem.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if int(Golem.frame) == 7 :
            Golem.add_event(UNCONTACT)



    def draw(Golem):
        Golem.sizex = 100
        Golem.sizey = 80
        Golem.image = load_image('Monster/Golem/golem-attack1.png')
        Golem.image.clip_draw(int(Golem.frame) * Golem.sizex, Golem.direction * Golem.sizey, Golem.sizex, Golem.sizey, int(Golem.x), int(Golem.y))

next_state_table = {
    IdleState: {CONTACT: AttackState},
    AttackState: {UNCONTACT: IdleState},

}

class Golem():
    def __init__(self):
        self.image = load_image('Monster/Golem/golem-attack1.png')

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
        if state == 'contact' and self.cur_state == IdleState:
            self.add_event(CONTACT)
            if self.direction == 3:
                self.x -= 5

            elif self.direction == 2:
                self.x += 5

            elif self.direction == 0:
                self.y -= 5

            elif self.direction == 1:
                self.y += 5

            return ''
        elif state == 'contact' and self.cur_state == AttackState and int(self.frame) == 6:
            return 'G_Attack'

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



