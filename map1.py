from pico2d import *
import game_framework
import random
import classMan
import classMon
import door

MAP_WIDTH, MAP_HEIGHT = 1276, 717
WALL_L, WALL_R = 150, 1130
WALL_U, WALL_D = 635, 85

rMon = None
tMon = None
man = None
map1 = None
Door = None

def enter():
    global rMon, tMon, man, map1, Door
    global MAP_HEIGHT, MAP_HEIGHT
    open_canvas(MAP_WIDTH, MAP_HEIGHT)
    man = classMan.Man()
    Door = door.door()
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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            man.handle_event(event)

def update():
    global rMon, tMon, man, Door
    for RMon in rMon:
        RMon.move()
    for TMon in tMon:
        TMon.move(man.x, man.y)
    man.update()
    Door.update()

def draw():
    clear_canvas()
    map1.draw(MAP_WIDTH//2, MAP_HEIGHT//2)
    man.draw()
    Door.draw()
    for RMon in rMon:
        RMon.draw()
    for TMon in tMon:
        TMon.draw()
    update_canvas()
    delay(0.05)