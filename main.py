from pico2d import *
import game_framework
import start_state

MAP_WIDTH, MAP_HEIGHT = 1276, 717


def main():
    pico2d.open_canvas(1276, 717)
    game_framework.run(start_state)
    pico2d.close_canvas()

if __name__ == '__main__':
    main()