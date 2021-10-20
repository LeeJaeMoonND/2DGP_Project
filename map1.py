from pico2d import *
import game_framework
import random
import start_state
import classMan
import classMon

MAP_WIDTH, MAP_HEIGHT = 1276, 717

rMon = None
tMon = None
man = None
map1 = None

def enter():
    global rMon, tMon, man, map1
    global MAP_HEIGHT, MAP_HEIGHT
    open_canvas(MAP_WIDTH, MAP_HEIGHT)
    man = classMan.Man()
    rMon = [classMon.RMon() for i in range(random.randint(0, 5))]
    tMon = [classMon.TMon() for i in range(random.randint(1, 1))]
    map1 = load_image('map1.png')

def exit():
    global rMon, tMon, man, map1
    del(rMon)
    del(tMon)
    del(man)
    del(map1)

def handle_events():
    global man

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RIGHT:
                man.move('MR')
            elif event.key == SDLK_LEFT:
                man.move('ML')
            elif event.key == SDLK_DOWN:
                man.move('MD')
            elif event.key == SDLK_UP:
                man.move('MU')
            elif event.key == SDLK_z:
                man.attack()
            # 구르기 미완성
            # elif event.key == SDLK_a:
            #     man.rolling()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                man.move('SR')
            elif event.key == SDLK_LEFT:
                man.move('SL')
            elif event.key == SDLK_DOWN:
                man.move('SD')
            elif event.key == SDLK_UP:
                man.move('SU')
def update():
    global rMon, tMon, man
    for RMon in rMon:
        RMon.move()
    for TMon in tMon:
        TMon.move(man.x, man.y)
    man.location()

def draw():
    clear_canvas()
    map1.draw(MAP_WIDTH//2, MAP_HEIGHT//2)
    man.draw()
    for RMon in rMon:
        RMon.draw()
    for TMon in tMon:
        TMon.draw()
    update_canvas()
    delay(0.05)