from pico2d import *

open_canvas()           # FRAME * 110, 1030, 160, 170, x, 120

character = load_image('animation_sheet.png')
grass = load_image('back_ground_forest.png')
HP_bar = load_image('HP_bar_2.jpg')

running = True
x = 400
y = 0
dir = 0
dir_y = 0
i = 0
vector = 3
frame = 0
adjust_on = False

def handle_events():
    global running
    global dir
    global dir_y
    global adjust_on
    global vector
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
                vector = 1
            elif event.key == SDLK_LEFT:
                dir -= 1
                vector = 0
            elif event.key == SDLK_x:
                work_adjust_jump()
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
                vector = 3
            elif event.key == SDLK_LEFT:
                dir += 1
                vector = 2

def adjust_jump():
    global dir_y
    global adjust_on

    if(adjust_on):
        dir_y += 1
    elif(adjust_on != True and dir_y >= 1):
        dir_y -= 1

    if (dir_y >= 10):
        adjust_on = False

def work_adjust_jump():
    global adjust_on
    global dir_y

    if dir_y == 0:
        adjust_on = True

while running :
    clear_canvas()
    grass.draw(400, 30)
    HP_bar.draw(100, 660)
    character.clip_draw(frame * 100, vector * 100, 100, 100, x, 90 + y)
    update_canvas()
    handle_events()
    adjust_jump()
    frame = (frame + 1) % 8
    x += dir * 5
    y = dir_y * 13
    delay(0.03)

close_canvas()