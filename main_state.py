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

slime = None
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
    global slime, golem, man, map1, Door
    global MAP_HEIGHT, MAP_HEIGHT
    global localX, localY
    open_canvas(MAP_WIDTH, MAP_HEIGHT)

    map1 = Map.Map()
    man = Man.Man()
    Door = door.door()
    slime = [Slime.slime() for i in range(SNum[localY][localX])]
    golem = [Golem.Golem() for i in range(GNum[localY][localX])]
    game_world.add_object(map1, 0)
    game_world.add_object(Door, 1)
    game_world.add_object(man, 2)
    game_world.add_objects(slime, 2)
    game_world.add_objects(golem, 2)
    print(game_world.objects)


def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global localx, localy, slime
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            man.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_u:
            for i in slime:
                slime.remove(i)
                game_world.remove_object(i)
            print(slime)
            if slime == [] :
                Door.set_open()


def update():
    global slime, golem
    global localY


    if collide(man, Door) and Door.get_open():
        slime = [Slime.slime() for i in range(SNum[localY][localX])]
        golem = [Golem.Golem() for i in range(GNum[localY][localX])]
        localY -= 1
        game_world.add_objects(slime, 2)
        game_world.add_objects(golem, 2)
        man.y = WALL_D

    if golem != None:
        for Golem1 in golem:
            Golem1.Dx, Golem1.Dy = man.x, man.y
    for Golem1 in golem :
        if Golem1.hp == 0:
            golem.remove(Golem1)
            game_world.remove_object(Golem1)

        if collide(man, Golem1):
            now = Golem1.change_state('contact')
            if man.get_curstate() == 'AttackState':
                Golem1.hited()
            else:
                if now == 'G_Attack':
                    man.hp -= 1

        for Slime1 in slime :
            for Golem1 in golem:
                if collide(Slime1, Golem1):
                    if Slime1.direction == 3:
                        Slime1.x = Golem1.x - Slime1.sizex
                    elif Slime1.direction == 2:
                        Slime1.x = Golem1.x + Slime1.sizex

                    elif Slime1.direction == 0:
                        Slime1.y = Golem1.y + Slime1.sizey

                    elif Slime1.direction == 1:
                        Slime1.y = Golem1.y - Slime1.sizey


    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()