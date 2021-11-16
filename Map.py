from pico2d import *
import random

import Slime


MAP_WIDTH, MAP_HEIGHT = 1276, 717


class Map:
    def __init__(self):
        self.image = load_image('map1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1276//2, 717//2)
