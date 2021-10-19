from pico2d import *
import random


KPU_WIDTH, KPU_HEIGHT = 1280, 1024

# 주인공
class Man():
    def __init__(self):
        self.image = load_image('man.png')
        self.frame = 0
        self.direction=0
        self.p = (self.x, self.y) = (400, 400)
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

# Random한 좌표를 지나는 몬스터
class RMon():
    def __init__(self):
        self.image = load_image('mon1.png')
        self.frame = 0
        self.direction = 8
        self.p1 = [random.randint(0, 800), random.randint(0, 600)]
        self.p2 = [random.randint(0, 800), random.randint(0, 600)]
        self.p3 = [random.randint(0, 800), random.randint(0, 600)]
        self.p4 = [random.randint(0, 800), random.randint(0, 600)]
        self.x, self.y = self.p2[0], self.p2[1]
        self.t = 0

    def draw(self):
        self.image.clip_draw(self.frame*134, self.direction*135, 134, 135, self.x, self.y)

    def move(self):
        self.x = ((-self.t**3 + 2*self.t**2 - self.t)*self.p1[0] + (
                3*self.t**3 - 5*self.t**2 + 2)*self.p2[0] + (
                -3*self.t**3 + 4*self.t**2 + self.t)*self.p3[0] + (self.t**3 - self.t**2)*self.p4[0])/2

        self.y = ((-self.t**3 + 2*self.t**2 - self.t)*self.p1[1] + (
                3*self.t**3 - 5*self.t**2 + 2)*self.p2[1] + (
                -3*self.t**3 + 4*self.t**2 + self.t)*self.p3[1] + (self.t**3 - self.t**2)*self.p4[1])/2

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
        self.x, self.y = random.randint(0,800) , random.randint(0,600)
        self.t = 0

    def draw(self):
        self.image.clip_draw(self.frame*134, self.direction*135, 134, 135, self.x, self.y)

    def move(self, Tx, Ty):
        self.t = (1000-abs(Tx-self.x))/50000
        self.x = (self.t * Tx) + (1-self.t) * self.x

        self.y = (self.t * Ty) + (1-self.t) * self.y

        self.frame = (self.frame + 1) % 5


def handle_events():
    global running
    global man

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                man.move('MR')
            elif event.key == SDLK_LEFT:
                man.move('ML')
            elif event.key == SDLK_DOWN:
                man.move('MD')
            elif event.key == SDLK_UP:
                man.move('MU')
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                man.move('SR')
            elif event.key == SDLK_LEFT:
                man.move('SL')
            elif event.key == SDLK_DOWN:
                man.move('SD')
            elif event.key == SDLK_UP:
                man.move('SU')


open_canvas()
man = Man()
Rmon1 = RMon()
Rmon2 = RMon()
running = True
Tmon1 = TMon()

while running:

    clear_canvas()
    man.draw()
    Rmon1.draw()
    Rmon2.draw()
    Tmon1.draw()
    update_canvas()
    handle_events()
    man.location()
    Rmon1.move()
    Rmon2.move()
    Tmon1.move(man.x, man.y)

    delay(0.03)
