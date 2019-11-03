from pico2d import *
import game_framework
import title_state

name = 'GameOverState'
image = None


def enter():
    global image
    image = load_image('Game Over Screen.png')


def exit():
    global image
    del image


def draw():
    global image
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)