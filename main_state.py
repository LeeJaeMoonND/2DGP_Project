from pico2d import *
import random

import game_world
import game_framework

import Map
import Man
import Golem
import door
import Slime

MAP_WIDTH, MAP_HEIGHT = 1276, 717
WALL_L, WALL_R = 150, 1130
WALL_U, WALL_D = 635, 85

name = 'MainState'

rMon = None
golem = None
man = None
map1 =  None
Door = None

map_logic = [[1, 1, 0],
             [0, 1, 0],
             [0, 1, 1]]
SNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]
GNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

for i in range(0,3):
    for j in range(0,3):
        if map_logic[j][i]==1:
            SNum[j][i] = random.randint(1, 5)
            GNum[j][i] = random.randint(1, 5)
print(SNum)

localX, localY = 1, 1

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def enter():
    global map_logic, SNum, GNum
    global rMon, golem, man, map1, Door
    global MAP_HEIGHT, MAP_HEIGHT
    global localX, localY
    open_canvas(MAP_WIDTH, MAP_HEIGHT)

    map1 = Map.Map()
    man = Man.Man()
    Door = door.door()
    rMon = [Slime.RMon() for i in range(SNum[localY][localX])]
    golem = [Golem.Golem() for i in range(GNum[localY][localX])]
    game_world.add_object(map1, 0)
    game_world.add_object(Door, 1)
    game_world.add_object(man, 2)
    game_world.add_objects(rMon, 2)
    game_world.add_objects(golem, 2)
    print(game_world.objects)


def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global localx, localy, rMon
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            man.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_u:
            for i in rMon:
                rMon.remove(i)
                game_world.remove_object(i)
            print(rMon)
            if rMon == [] :
                Door.set_open()




def update():
    global rMon, golem
    global localY
    if collide(man, Door) and Door.get_open():
        for i in rMon:
            game_world.remove_object(i)
        localY -= 1
        rMon = [Slime.RMon() for j in range(SNum[localY][localX])]
        game_world.add_objects(rMon, 2)
        man.y = WALL_D

    if golem != None:
        for Golem in golem:
            Golem.Dx, Golem.Dy = man.x, man.y
    for Golem in golem :
        if collide(man, Golem):
            now = Golem.change_state('contact')
            if now == 'G_Attack':
                man.hp -= 1
                man.x


    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()