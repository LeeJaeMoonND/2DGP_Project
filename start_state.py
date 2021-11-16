from pico2d import *
import game_framework
import main_state

MAP_WIDTH, MAP_HEIGHT = 1276, 717

name = "StartState"
image = None

def enter():
    global image
    image = load_image('start.png')


def exit():
    global image
    del(image)

def update():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    global image
    clear_canvas()
    image.draw(MAP_WIDTH//2, MAP_HEIGHT//2)
    update_canvas()


def pause(): pass


def resume(): pass