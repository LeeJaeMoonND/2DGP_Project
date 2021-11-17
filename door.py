from pico2d import *
import game_framework

OPEN, CLOSE = range(2)
MAP_WIDTH, MAP_HEIGHT = 1276, 717
WALL_L, WALL_R = 150, 1130
WALL_U, WALL_D = 635, 85



class OpenState:
    def enter(door, event):
        door.time = 100

    def exit(door, event):
        pass

    def do(door):
        pass

    def draw(door):
        if door.location == 'up':
            door.image = load_image('door/door_up_open.png')
            door.image.draw(door.x, door.y, 142, 90)
        elif door.location == 'left':
            door.image = load_image('door/door_left_open.png')
            door.image.draw(door.x, door.y, 90, 142)
        elif door.location == 'down':
            door.image = load_image('door/door_down_open.png')
            door.image.draw(door.x, door.y, 142, 90)
        elif door.location == 'right':
            door.image = load_image('door/door_right_open.png')
            door.image.draw(door.x, door.y, 90, 142)

class CloseState:
    def enter(door, event):
        door.time = 100

    def exit(door, event):
        pass

    def do(door):
        pass

    def draw(door):
        if door.location == 'up':
            door.image = load_image('door/door_up_close.png')
            door.image.draw(door.x, door.y, 142, 90)
        elif door.location == 'left':
            door.image = load_image('door/door_left_close.png')
            door.image.draw(door.x, door.y, 90, 142)
        elif door.location == 'down':
            door.image = load_image('door/door_down_close.png')
            door.image.draw(door.x, door.y, 142, 90)
        elif door.location == 'right':
            door.image = load_image('door/door_right_close.png')
            door.image.draw(door.x, door.y, 90, 142)


next_state_table = {
    OpenState: {CLOSE: CloseState, OPEN:OpenState},
    CloseState: {OPEN: OpenState, CLOSE: CloseState}
}

class door():
    def __init__(self,location):
        self.location = location
        if self.location == 'up':
            self.image = load_image('door/door_up_open.png')
            self.p = (self.x, self.y) = MAP_WIDTH//2, WALL_U+38
        elif self.location == 'left':
            self.image = load_image('door/door_left_open.png')
            self.p = (self.x, self.y) = WALL_L-20, MAP_HEIGHT//2
        elif self.location == 'down':
            self.image = load_image('door/door_down_open.png')
            self.p = (self.x, self.y) = MAP_WIDTH//2, WALL_D-38

        elif self.location == 'right':
            self.image = load_image('door/door_right_open.png')
            self.p = (self.x, self.y) = WALL_R+20, MAP_HEIGHT//2

        self.event_que = []
        self.cur_state = CloseState
        self.cur_state.enter(self, None)

    def get_bb(self):
        if self.location == 'up' or self.location == 'down' :
            return self.x - 50, self.y-10, self.x + 50, self.y + 45
        elif self.location == 'left' or self.location == 'right' :
            return self.x - 10, self.y - 50, self.x + 10, self.y + 50


    def set_open(self):
        self.add_event(OPEN)
    def set_close(self):
        self.add_event(CLOSE)

    def get_open(self):
        if self.cur_state == OpenState:
            return True
        else:
            return False


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

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
       pass





