from pico2d import *



MAP_WIDTH, MAP_HEIGHT = 1276, 717


class Gameover:
    def __init__(self):
        self.image = load_image('map/gameover.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1276//2, 717//2)
