from pico2d import *
import game_framework
import game_world
from FireBall import FireBall

import random

PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


MAP_WIDTH, MAP_HEIGHT = 1175, 585

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, A_DOWN, A_UP, Z_DOWN, Z_UP, TIME_OUT, SPACE_DOWN = range(14)
error = ['RIGHT_DOWN', 'LEFT_DOWN', 'UP_DOWN', 'DOWN_DOWN', 'RIGHT_UP', 'LEFT_UP', 'UP_UP', 'DOWN_UP', 'A_DOWN', 'A_UP', 'Z_DOWN', 'Z_UP', 'TIME_OUT', 'SPACE_DOWN']

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN) : DOWN_UP,
    (SDL_KEYDOWN, SDLK_a): A_DOWN,
    (SDL_KEYUP, SDLK_a): A_UP,
    (SDL_KEYDOWN, SDLK_z): Z_DOWN,
    (SDL_KEYUP, SDLK_z): Z_UP,
    (SDL_KEYUP, SDLK_SPACE): SPACE_DOWN
}


class IdleState:
    def enter(Man, event):
        if event == RIGHT_DOWN:
            Man.velocityX += RUN_SPEED_PPS
            Man.direction = 3
        elif event == LEFT_DOWN:
            Man.velocityX -= RUN_SPEED_PPS
            Man.direction = 2
        elif event == UP_DOWN:
            Man.velocityY += RUN_SPEED_PPS
            Man.direction = 0
        elif event == DOWN_DOWN:
            Man.velocityY -= RUN_SPEED_PPS
            Man.direction = 1
        elif event == RIGHT_UP:
            Man.velocityX -= RUN_SPEED_PPS
            Man.direction = 3
        elif event == LEFT_UP:
            Man.velocityX += RUN_SPEED_PPS
            Man.direction = 2
        elif event == UP_UP:
            Man.velocityY -= RUN_SPEED_PPS
            Man.direction = 0
        elif event == DOWN_UP:
            Man.velocityY += RUN_SPEED_PPS
            Man.direction = 1

    def exit(Man, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(Man):
        Man.image = load_image('will/Will_Idle35.35.png')
        Man.image.clip_draw(int(Man.frame) * 70, Man.direction * 70, 70, 70, int(Man.x), int(Man.y))

class RunState:

    def enter(Man, event):
        if event == RIGHT_DOWN:
            Man.velocityX += RUN_SPEED_PPS
            Man.direction = 3
        elif event == LEFT_DOWN:
            Man.velocityX -= RUN_SPEED_PPS
            Man.direction = 2
        elif event == UP_DOWN:
            Man.velocityY += RUN_SPEED_PPS
            Man.direction = 0
        elif event == DOWN_DOWN:
            Man.velocityY -= RUN_SPEED_PPS
            Man.direction = 1
        elif event == RIGHT_UP:
            Man.velocityX -= RUN_SPEED_PPS
            Man.direction = 3
        elif event == LEFT_UP:
            Man.velocityX += RUN_SPEED_PPS
            Man.direction = 2
        elif event == UP_UP:
            Man.velocityY -= RUN_SPEED_PPS
            Man.direction = 0
        elif event == DOWN_UP:
            Man.velocityY += RUN_SPEED_PPS
            Man.direction = 1

    def exit(boy, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Man.x += Man.velocityX * game_framework.frame_time
        Man.y += Man.velocityY * game_framework.frame_time
        Man.x = clamp(150, Man.x, 1130)
        Man.y = clamp(100, Man.y, 635)


    def draw(Man):
        Man.image = load_image('will/will animation cycle35.35.png')
        Man.image.clip_draw(int(Man.frame) * 70, Man.direction * 70, 70, 70, int(Man.x), int(Man.y))


class RollState:

    def enter(Man, event):
        if event == A_DOWN:
            Man.frame = 0

    def exit(boy, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Man.x += Man.velocityX * game_framework.frame_time * 1.5
        Man.y += Man.velocityY * game_framework.frame_time * 1.5
        if int(Man.frame) == 7:
            Man.add_event(TIME_OUT)
        Man.x = clamp(150, Man.x, 1130)
        Man.y = clamp(100, Man.y, 635)


    def draw(Man):
        Man.image = load_image('will/Will_Roll35.35.png')
        Man.image.clip_draw(int(Man.frame) * 70, Man.direction * 70, 70, 70, int(Man.x), int(Man.y))

class AttackState:
    def enter(Man, event):
        if event == Z_DOWN:
            Man.frame = 0
        if event == SPACE_DOWN:
            Man.fire_ball()

    def exit(Man, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if int(Man.frame) == 7:
            Man.add_event(TIME_OUT)

    def draw(Man):
        Man.image = load_image('will/will_attack.png')
        Man.image.clip_draw(int(Man.frame) * 70, Man.direction * 110, 70, 110, int(Man.x), int(Man.y))

class MagicState:
    def enter(Man, event):
        if event == SPACE_DOWN:
            Man.frame = 0
            Man.fire_ball()

    def exit(Man, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if int(Man.frame) == 7:
            Man.add_event(TIME_OUT)

    def draw(Man):
        Man.image = load_image('will/will_attack.png')
        Man.image.clip_draw(int(Man.frame) * 70, Man.direction * 110, 70, 110, int(Man.x), int(Man.y))

next_state_table = {
    IdleState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP:IdleState,DOWN_UP:IdleState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState,UP_DOWN:RunState,DOWN_DOWN:RunState,
    A_DOWN:RollState, A_UP:IdleState, Z_DOWN: AttackState, Z_UP: IdleState,SPACE_DOWN:MagicState},

    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP:IdleState, DOWN_UP: IdleState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN: RunState, DOWN_DOWN: RunState,
    A_DOWN: RollState, A_UP: RunState, Z_DOWN: AttackState, Z_UP: IdleState,TIME_OUT: RunState,SPACE_DOWN:MagicState},

    RollState:{RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP:IdleState,DOWN_UP:IdleState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState,UP_DOWN:RunState,DOWN_DOWN:RunState,TIME_OUT:RunState,
    A_DOWN:RollState, A_UP: RollState, Z_DOWN:RollState, Z_UP:RollState,SPACE_DOWN:MagicState},

    AttackState:{RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState,DOWN_UP: IdleState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN:RunState, DOWN_DOWN:RunState, TIME_OUT: RunState,
    A_DOWN: RollState, A_UP: RollState, Z_UP: AttackState, TIME_OUT: IdleState,SPACE_DOWN:MagicState},

    MagicState:{RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState,DOWN_UP: IdleState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState, UP_DOWN:RunState, DOWN_DOWN:RunState, TIME_OUT: RunState,
    A_DOWN: RollState, A_UP: RollState, Z_UP: AttackState, TIME_OUT: IdleState,SPACE_DOWN:MagicState}
}


class Man():
    def __init__(self):
        self.image = load_image('will/will animation cycle35.35.png')
        self.frame = 0
        # 움직임
        self.dir = 0
        self.direction = 0

        # 좌표, 방향
        self.velocityX = 0
        self.velocityY = 0
        self.p = (self.x, self.y) = (MAP_WIDTH / 2, MAP_HEIGHT / 2)

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        self.font=load_font('ENCR10B.TTF',16)

        # 아직 생각만 하고 있는 능력치
        self.hp = 100
        self.mp = 100
        self.damage = 5

    def get_curstate(self):
        if self.cur_state == IdleState:
            return 'IdleState'
        elif self.cur_state == RunState:
            return 'RunState'
        elif self.cur_state == RollState:
            return 'RollState'
        elif self.cur_state == AttackState:
            return 'AttackState'

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def change_state(self, state):
        pass

    def fire_ball(self):
        if self.mp >= 10:
            fireball = FireBall(self.x, self.y, self.direction)
            game_world.add_object(fireball, 2)
            self.mp -= 10


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.mp += 0.02
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            try:
                self.cur_state.exit(self, event)
                self.cur_state = next_state_table[self.cur_state][event]
                self.cur_state.enter(self, event)
            except:
                print(self.cur_state, error[event])

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity: ' + str(self.velocityX) + ' Dir:' + str(self.dir))
        self.font.draw(self.x - 30, self.y + 65, 'HP: %d' %self.hp,(255, 255, 0))
        self.font.draw(self.x - 30, self.y + 50, 'MP: %d' %self.mp,(255, 255, 0))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

