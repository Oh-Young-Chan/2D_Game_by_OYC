from pico2d import *
import game_framework
import title_state

width = 1280 // 2
height = 720 // 2

name = 'StartState'
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('image\kpu_credit.png')


def exit():
    global image
    del image


def update():
    global logo_time

    if logo_time > 1.0:
        logo_time = 0
        game_framework.change_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    global image
    global width, height
    clear_canvas()
    image.draw(width, height)
    update_canvas()


def handle_events():
    events = get_events()


def pause():
    pass


def resume():
    pass
