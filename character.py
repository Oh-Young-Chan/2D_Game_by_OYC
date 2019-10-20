from pico2d import *

open_canvas()           # FRAME * 110, 1030, 160, 170, x, 120

character = load_image('character_animation.png')
ground_start = load_image('ground1x1.png')
ground = load_image('ground1x2.png')
flatform1of3 = load_image('flatform1x1.png')
flatform2of3 = load_image('flatform1x2.png')
flatform3of3 = load_image('flatform1x3.png')
background = load_image('back.png')
HP_bar = load_image('HP_bar.png')
damaged_HP_bar = load_image('Damaged_HP_Bar_part.png')
spike = load_image('spike.png')

running = True
damaging = False
form = True
flat = False
HP = 100
hit_count = 0
x = 400
y = 0
f_y = 0
dir = 0
dir_y = 0
i = 0
vector = 6
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
                vector = 4
            elif event.key == SDLK_LEFT:
                dir -= 1
                vector = 5
            elif event.key == SDLK_x:
                work_adjust_jump()
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
                vector = 6
            elif event.key == SDLK_LEFT:
                dir += 1
                vector = 7

def flatform():
    global f_y
    global form
    global flat
    if (x>180 and x < 290 and y <= 130):
        if form:
            f_y += 88
            form = False
            flat = True
    else:
        if flat:
            f_y -= 88
            flat = False
            form = True

def damaged(damaged):
    global vector
    global hit_count
    hit_count += 1
    decrease_HP(damaged)
    if (vector == 4):
        vector = 0
        character.clip_draw(frame * 96, vector * 96, 96, 96, x, 90 + y)
    elif (vector == 5):
        vector = 1
        character.clip_draw(frame * 96, vector * 96, 96, 96, x, 90 + y)

def decrease_HP(damage):
    global HP
    global damaging
    HP -= damage
    damaging = True

def black_HP():
    if damaging:
        for i in range(hit_count):
            if i <= 21:
                fill_black_HP(i)

def fill_black_HP(i):
    damaged_HP_bar.draw(263 - i * 11, 550)

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
    background.draw(400, 300)
    ground_start.draw(0, 30)
    flatform1of3.draw(200, 130)
    flatform2of3.draw(232, 130)
    flatform3of3.draw(264, 130)
    flatform()
    for i in range(15):
        ground.draw(64 + i*64, 30)
    HP_bar.draw(150, 550)
    spike.draw(600, 70)
    if (x > 580 and x < 620 and y <= 50):
        damaged(50)
    character.clip_draw(frame * 96, vector * 96, 96, 96, x, 90 + y + f_y)
    black_HP()
    update_canvas()
    handle_events()
    adjust_jump()
    frame = (frame + 1) % 5
    x += dir * 5
    y = dir_y * 13
    delay(0.03)

close_canvas()