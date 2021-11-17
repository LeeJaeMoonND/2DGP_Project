from pico2d import *
import random

import game_world
import game_framework

import gameover
import Map
import Man
import Golem
import Turret
import door
import Slime
import Rock

MAP_WIDTH, MAP_HEIGHT = 1276, 717
WALL_L, WALL_R = 150, 1130
WALL_U, WALL_D = 635, 85

name = 'MainState'

slime = None
golem = None
turret = None
man = None
map =  None
Door = [[], [], [], []]
rock = []

map_logic = [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0]]

SNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

GNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

TNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]
RNum = [[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]]

RLocx = []

RLocy = []

for i in range(1,5):
    for j in range(1,5):
        if map_logic[j][i]==1:
            SNum[j-1][i-1] = random.randint(1, 5)
            GNum[j-1][i-1] = random.randint(1, 3)
            TNum[j-1][i-1] = random.randint(1, 3)
            RNum[j-1][i-1] = random.randint(1, 3)

print(SNum,GNum,TNum,RNum)

localX, localY = 1, 3

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def draw_dooor(o):
    global localX, localY

    if map_logic[localY - 1][localX] == 1:
        game_world.add_object(o[0], 1)
        o[0].set_close()
    if map_logic[localY + 1][localX] == 1:
        game_world.add_object(o[1], 1)
        o[1].set_close()
    if map_logic[localY][localX - 1] == 1:
        game_world.add_object(o[2], 1)
        o[2].set_close()
    if map_logic[localY][localX + 1] == 1:
        game_world.add_object(o[3], 1)
        o[3].set_close()
    print(localX,localY)


def enter():
    global map_logic, SNum, GNum, TNum, RNum, RLocx,RLocy
    global slime, golem, man, map, Door, turret, rock
    global MAP_HEIGHT, MAP_HEIGHT
    global localX, localY
    open_canvas(MAP_WIDTH, MAP_HEIGHT)

    map = Map.Map()
    man = Man.Man()
    Door[0] = door.door('up')
    Door[1] = door.door('down')
    Door[2] = door.door('left')
    Door[3] = door.door('right')

    if map_logic[localY-1][localX] == 1 :
        game_world.add_object(Door[0], 1)
    if map_logic[localY+1][localX] == 1:
        game_world.add_object(Door[1], 1)
    if map_logic[localY][localX-1] == 1:
        game_world.add_object(Door[2], 1)
    if map_logic[localY][localX+1] == 1:
        game_world.add_object(Door[3], 1)
    print(Door)
    for i in range(RNum[localY-1][localX-1]):
        RLocx.append(random.randint(150, 1130))
        RLocy.append(random.randint(85, 635))
    rock = [Rock.Rock(RLocx[i], RLocy[i]) for i in range(RNum[localY-1][localX-1])]
    slime = [Slime.slime() for i in range(SNum[localY-1][localX-1])]
    golem = [Golem.Golem() for i in range(GNum[localY-1][localX-1])]
    turret = [Turret.Turret() for i in range(TNum[localY-1][localX-1])]

    game_world.add_object(map, 0)

    game_world.add_object(man, 2)
    game_world.add_objects(slime, 2)
    game_world.add_objects(golem, 2)
    game_world.add_objects(turret, 2)
    game_world.add_objects(rock, 1)
    print(game_world.objects)


def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global localX, localY, slime, SNum
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
                SNum[localY-1][localX-1] -= 1
                slime.remove(i)
                game_world.remove_object(i)
            print(SNum)




def update():
    global slime, golem, man, turret,rock
    global Door
    global localY, localX
    global SNum, GNum, TNum, RNum, RLocx, RLocy

    if SNum[localY-1][localX-1] == 0 and GNum[localY-1][localX-1] == 0 and TNum[localY-1][localX-1] == 0:
        if map_logic[localY - 1][localX] == 1:
            Door[0].set_open()
        if map_logic[localY + 1][localX] == 1:
            Door[1].set_open()
        if map_logic[localY][localX - 1] == 1:
            Door[2].set_open()
        if map_logic[localY][localX + 1] == 1:
            Door[3].set_open()
    if man.hp <= 0:
        game_world.clear()
        gameover1= gameover.Gameover()
        game_world.add_object(gameover1, 1)
        game_world.add_object(map, 0)


    if collide(man, Door[0]) and Door[0].get_open() and map_logic[localY - 1][localX] == 1:
        localY -= 1
        man.y = WALL_D + 50
        for i in slime:
            slime.remove(i)
        for i in golem:
            golem.remove(i)
        for i in turret:
            turret.remove(i)
        for i in rock:
            rock.remove(i)

        RLocx.clear()
        RLocy.clear()
        for i in range(RNum[localY - 1][localX - 1]):
            RLocx.append(random.randint(150, 1130))
            RLocy.append(random.randint(85, 635))
        rock = [Rock.Rock(RLocx[i], RLocy[i]) for i in range(RNum[localY - 1][localX - 1])]
        turret = [Turret.Turret() for i in range(TNum[localY - 1][localX - 1])]
        slime = [Slime.slime() for i in range(SNum[localY - 1][localX - 1])]
        golem = [Golem.Golem() for i in range(GNum[localY - 1][localX - 1])]

        game_world.clear()

        game_world.add_object(map, 0)
        game_world.add_objects(slime, 2)
        game_world.add_objects(golem, 2)
        game_world.add_objects(turret, 2)
        game_world.add_objects(rock, 1)
        game_world.add_object(man, 2)

        draw_dooor(Door)

    if collide(man, Door[1]) and Door[1].get_open() and map_logic[localY + 1][localX] == 1:

        localY += 1
        man.y = WALL_U -50
        for i in slime:
            slime.remove(i)
        for i in golem:
            golem.remove(i)
        for i in turret:
            turret.remove(i)
        for i in rock:
            rock.remove(i)

        RLocx.clear()
        RLocy.clear()
        for i in range(RNum[localY - 1][localX - 1]):
            RLocx.append(random.randint(150, 1130))
            RLocy.append(random.randint(85, 635))
        rock = [Rock.Rock(RLocx[i], RLocy[i]) for i in range(RNum[localY - 1][localX - 1])]
        turret = [Turret.Turret() for i in range(TNum[localY - 1][localX - 1])]
        slime = [Slime.slime() for i in range(SNum[localY - 1][localX - 1])]
        golem = [Golem.Golem() for i in range(GNum[localY - 1][localX - 1])]

        game_world.clear()

        game_world.add_object(map, 0)
        game_world.add_objects(slime, 2)
        game_world.add_objects(golem, 2)
        game_world.add_objects(turret, 2)
        game_world.add_objects(rock, 1)
        game_world.add_object(man, 2)

        draw_dooor(Door)

    if collide(man, Door[2]) and Door[2].get_open() and map_logic[localY][localX - 1] == 1:

        localX -= 1
        man.x = WALL_R -50
        for i in slime:
            slime.remove(i)
        for i in golem:
            golem.remove(i)
        for i in turret:
            turret.remove(i)
        for i in rock:
            rock.remove(i)

        RLocx.clear()
        RLocy.clear()
        for i in range(RNum[localY - 1][localX - 1]):
            RLocx.append(random.randint(150, 1130))
            RLocy.append(random.randint(85, 635))
        rock = [Rock.Rock(RLocx[i], RLocy[i]) for i in range(RNum[localY - 1][localX - 1])]
        turret = [Turret.Turret() for i in range(TNum[localX - 1][localY])]
        slime = [Slime.slime() for i in range(SNum[localY - 1][localX - 1])]
        golem = [Golem.Golem() for i in range(GNum[localY - 1][localX - 1])]

        game_world.clear()

        game_world.add_object(map, 0)
        game_world.add_objects(slime, 2)
        game_world.add_objects(golem, 2)
        game_world.add_objects(turret, 2)
        game_world.add_objects(rock, 1)
        game_world.add_object(man, 2)

        draw_dooor(Door)


    if collide(man, Door[3]) and Door[3].get_open() and map_logic[localY][localX + 1] == 1:
        localX += 1
        man.y = WALL_L+50

        for i in slime:
            slime.remove(i)
        for i in golem:
            golem.remove(i)
        for i in turret:
            turret.remove(i)
        for i in rock:
            rock.remove(i)

        RLocx.clear()
        RLocy.clear()
        for i in range(RNum[localY - 1][localX - 1]):
            RLocx.append(random.randint(150, 1130))
            RLocy.append(random.randint(85, 635))

        rock = [Rock.Rock(RLocx[i], RLocy[i]) for i in range(RNum[localY - 1][localX - 1])]
        turret = [Turret.Turret() for i in range(TNum[localY - 1][localX - 1])]
        slime = [Slime.slime() for i in range(SNum[localY - 1][localX - 1])]
        golem = [Golem.Golem() for i in range(GNum[localY - 1][localX - 1])]

        game_world.clear()

        game_world.add_object(map, 0)
        game_world.add_objects(slime, 2)
        game_world.add_objects(golem, 2)
        game_world.add_objects(turret, 2)
        game_world.add_objects(rock, 1)
        game_world.add_object(man, 2)


        draw_dooor(Door)

    if turret != None:
        for turret1 in turret:
            turret1.Dx, turret1.Dy = man.x, man.y
            if turret1.hp <= 0:
                TNum[localY - 1][localX - 1] -= 1
                turret.remove(turret1)
                game_world.remove_object(turret1)

            for turretball in turret1.turretball:
                if collide(turretball, man):
                    man.hp -= 5
                    turret1.turretball.remove(turretball)
                    game_world.remove_object(turretball)
                    turret1.TSq -= 1

            if collide(man, turret1):
                if man.get_curstate() == 'AttackState':
                    turret1.hited(2, man.damage)
            for fire1 in man.fireball:
                if collide(fire1, turret1):
                    turret1.hited(1, fire1.damage)

    if golem != None:
        for Golem1 in golem:
            Golem1.Dx, Golem1.Dy = man.x, man.y
    for Golem1 in golem :
        if Golem1.hp <= 0:
            GNum[localY-1][localX-1] -= 1
            golem.remove(Golem1)
            game_world.remove_object(Golem1)

        if collide(man, Golem1):
            now = Golem1.change_state('contact')
            if man.get_curstate() == 'AttackState':
                Golem1.hited(5, man.damage)
            else:
                if now == 'G_Attack':
                    man.hp -= 1
        for fire1 in man.fireball:
            if collide(fire1, Golem1):
                Golem1.hited(1, fire1.damage)


            for Slime1 in slime :
                if collide(Slime1, Golem1):
                    if Slime1.direction == 3:
                        Slime1.x = Golem1.x - Slime1.sizex
                    elif Slime1.direction == 2:
                        Slime1.x = Golem1.x + Slime1.sizex

                    elif Slime1.direction == 0:
                        Slime1.y = Golem1.y + Slime1.sizey

                    elif Slime1.direction == 1:
                        Slime1.y = Golem1.y - Slime1.sizey
        '''
        오류
        for Golem2 in golem :
            if Golem1.x == Golem2.x:
                pass
            else:
                if Golem2.direction == 3:
                    Golem2.x -= 5
                elif Golem2.direction == 2:
                    Golem2.x += 5
                elif Golem2.direction == 0:
                    Golem2.y -= 5
                elif Golem2.direction== 1:
                    Golem2.y += 5
        '''
    '''for rocks in rock:
        rocks.dir = 0
        if collide(rocks, man):
            if man.get_curstate() != 'RollState':
                if man.direction == 1 :
                    man.velocityY = 0
        rocks.dir = 1
        if collide(rocks, man):
            if man.get_curstate() != 'RollState':
                if man.direction == 0:
                    man.velocityY = 0
        rocks.dir = 2
        if collide(rocks, man):
            if man.get_curstate() != 'RollState':
                if man.direction == 3:
                    man.velocityX = 0
        rocks.dir = 3
        if collide(rocks, man):
            if man.get_curstate() != 'RollState':
                if man.direction == 2:
                    man.velocityY = 0
    '''


    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()