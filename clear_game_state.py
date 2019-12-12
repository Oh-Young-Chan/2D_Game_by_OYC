from pico2d import *
import game_framework
import title_state

width = 1280 // 2
height = 720 // 2

name = 'ClearGameState'
endImage = None
congImage = None
characterImage = None


def enter():
    global endImage, congImage, characterImage
    endImage = load_image('image\end_screen.png')
    congImage = load_image('image\congratulations.png')
    characterImage = load_image('image\Pink_Monster.png')


def exit():
    global endImage, congImage, characterImage
    del image


def draw():
    global endImage, congImage, characterImage
    global width, height
    clear_canvas()
    endImage.draw(width, height)
    congImage.draw(width, 96)
    characterImage.draw(width, height)
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