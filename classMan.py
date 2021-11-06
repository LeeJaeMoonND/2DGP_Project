from pico2d import *
import random

MAP_WIDTH, MAP_HEIGHT = 1175, 585

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP = range(8)
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN) : DOWN_UP
}


class IdleState:
    def enter(Man, event):
        if event == RIGHT_DOWN:
            Man.velocityX += 1
            Man.direction = 3
        elif event == LEFT_DOWN:
            Man.velocityX -= 1
            Man.direction = 2
        elif event == UP_DOWN:
            Man.velocityY += 1
            Man.direction = 0
        elif event == DOWN_DOWN:
            Man.velocityY -= 1
            Man.direction = 1
        elif event == RIGHT_UP:
            Man.velocityX -= 1
            Man.direction = 3
        elif event == LEFT_UP:
            Man.velocityX += 1
            Man.direction = 2
        elif event == UP_UP:
            Man.velocityY -= 1
            Man.direction = 0
        elif event == DOWN_UP:
            Man.velocityY += 1
            Man.direction = 1

        Man.timer = 1000
    def exit(boy, event):
        pass
    def do(Man):
        Man.frame = (Man.frame + 1) % 8
        Man.timer -= 1
    def draw(Man):
        Man.image = load_image('Will_Idle35.35.png')
        Man.image.clip_draw(Man.frame * 70, Man.direction * 70, 70, 70, Man.x, Man.y)

class RunState:
    def enter(Man, event):
        if event == RIGHT_DOWN:
            Man.velocityX += 1
            Man.direction = 3
        elif event == LEFT_DOWN:
            Man.velocityX -= 1
            Man.direction = 2
        elif event == UP_DOWN:
            Man.velocityY += 1
            Man.direction = 0
        elif event == DOWN_DOWN:
            Man.velocityY -= 1
            Man.direction = 1
        elif event == RIGHT_UP:
            Man.velocityX -= 1
            Man.direction = 3
        elif event == LEFT_UP:
            Man.velocityX += 1
            Man.direction = 2
        elif event == UP_UP:
            Man.velocityY -= 1
            Man.direction = 0
        elif event == DOWN_UP:
            Man.velocityY += 1
            Man.direction = 1
        Man.timer = 1000

    def exit(boy, event):
        pass

    def do(Man):
        Man.frame = (Man.frame + 1) % 8
        Man.timer -= 1
        Man.x += Man.velocityX
        Man.y += Man.velocityY
        Man.x = clamp(25, Man.x, 800 - 25)
        Man.y = clamp(25, Man.y, 800 - 25)
    def draw(Man):

        Man.image = load_image('will animation cycle35.35.png')
        Man.image.clip_draw(Man.frame * 70, Man.direction * 70, 70, 70, Man.x, Man.y)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, UP_UP:RunState,DOWN_UP:RunState,
    RIGHT_DOWN: RunState, LEFT_DOWN: RunState,UP_DOWN:RunState,DOWN_DOWN:RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP:IdleState,DOWN_UP:IdleState,
    RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState,UP_DOWN:IdleState,DOWN_DOWN:IdleState},
}


class Man():
    def __init__(self):
        self.image = load_image('will animation cycle35.35.png')
        self.frame = 0
        # 움직임
        self.dir = 0
        self.direction=0

        # 좌표, 방향
        self.velocityX = 0
        self.velocityY = 0
        self.p = (self.x, self.y) = (MAP_WIDTH / 2, MAP_HEIGHT / 2)

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


        # 아직 생각만 하고 있는 능력치
        self.hp = 100
        self.mp = 100
        self.speed = 1
        self.damage = 5

    def change_state(self, state):
        # fill here
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

    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity: ' + str(self.velocityX) + ' Dir:' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

