from pico2d import *
import game_framework

OPEN, CLOSE = range(2)



class OpenState:
    def enter(door, event):
        door.time = 10

    def exit(door, event):
        pass

    def do(doorz):
        if door.time == 0:
            door.add_event(CLOSE)
        door.time -= 1



    def draw(door):
        door.image = load_image('door/golem_basic_doors10.png')
        door.image.draw(door.x, door.y,82,52)

class CloseState:
    def enter(door, event):
        door.time = 10

    def exit(door, event):
        pass

    def do(door):
        if door.time == 0:
            door.add_event(OPEN)
        door.time -= 1

    def draw(door):
        door.image = load_image('door/golem_basic_doors1.png')
        door.image.draw(door.x, door.y, 82, 52)


next_state_table = {
    OpenState: {CLOSE: CloseState},
    CloseState: {OPEN: OpenState},

}

class door():
    def __init__(self):
        self.image = load_image('door/golem_basic_doors1.png')
        self.p = (self.x, self.y) = 800, 500
        self.time = 100

        self.event_que = []
        self.cur_state = OpenState
        self.cur_state.enter(self, None)

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

    def handle_event(self, event):
       pass





