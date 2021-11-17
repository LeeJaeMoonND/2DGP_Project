from pico2d import *
import random

import Slime


MAP_WIDTH, MAP_HEIGHT = 1276, 717


class Rock:
    def __init__(self,x = 100, y = 100):
        self.image = load_image('map/rocks.png')
        self.shape = 0
        self.sizex,self.sizey = 60, 60
        self.x, self.y = x, y
        self.bb_dir = 0

    def get_bb(self):
        if self.bb_dir == 0:
            return self.x - (self.sizex // 2), self.y + (self.sizey // 2), self.x + (self.sizex // 2), self.y + (self.sizey // 2)
        elif self.bb_dir == 1:
            return self.x - (self.sizex // 2), self.y - (self.sizey // 2), self.x + (self.sizex // 2), self.y - (self.sizey // 2)
        elif self.bb_dir == 2:
            return self.x - (self.sizex // 2), self.y - (self.sizey // 2), self.x - (self.sizex // 2), self.y + (self.sizey // 2)
        elif self.bb_dir == 3:
            return self.x + (self.sizex // 2), self.y - (self.sizey // 2), self.x + (self.sizex // 2), self.y + (self.sizey // 2)

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.clip_draw(self.shape, 0, self.sizex, self.sizey, self.x, self.y)
