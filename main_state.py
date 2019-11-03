from pico2d import *
import game_framework
import game_over_state
import pause_state

running = True
i = 0
dir = 0
dir_y = 0
vector = 15
adjust_on = False


class Boy:
    def __init__(self):
        self.x, self.y = 400, 0
        self.frame = 0
        self.HP = 100
        self.vector = 15
        self.hit_count = 0
        self.image = load_image('Adventurer Sprite Sheet v1.1.png')

    def update(self, dir, dir_y, vector):
        self.frame = (self.frame+1) % 8
        self.x += dir * 5
        self.y = dir_y * 10
        self.vector = vector

    def draw(self):
        self.image.clip_draw(self.frame * 32, self.vector * 32, 32, 32, self.x, 108 + self.y, 100, 100)

    def damaged(self, damaged):
        self.HP -= damaged
        self.hit_count += 1
        hp_bar.decrease_HP()
        if (self.vector == 4):
            self.vector = 0
            self.image.clip_draw(self.frame * 96, self.vector * 96, 96, 96, self.x, 90 + self.y)
        elif (self.vector == 5):
            self.vector = 1
            self.image.clip_draw(self.frame * 96, self.vector * 96, 96, 96, self.x, 90 + self.y)

    def game_over(self):
        if self.HP <= 0:
            game_framework.change_state(game_over_state)



class Background:
    def __init__(self):
        self.x, self.y = 400, 300
        self.image = load_image('back.png')

    def draw(self):
        self.image.draw(self.x, self.y)


class Ground:
    def __init__(self):
        self.x, self.y = 0, 30
        self.image_start = load_image('ground1x1.png')
        self.image_middle = load_image('ground1x2.png')

    def draw(self):
        self.image_start.draw(0, self.y)
        for i in range(0, 11+1):
            self.image_middle.draw(64 + 64 * i, self.y)


class HP_BAR:
    def __init__(self):
        self.damaging = False
        self.image = load_image('HP_Bar.png')
        self.damaged_image = load_image('Damaged_HP_Bar_part.png')

    def draw(self):
        self.image.draw(150, 550)

    def decrease_HP(self):
        self.damaging = True


class Spike:
    def __init__(self):
        self.x, self.y = 700, 70
        self.image = load_image('spike.png')

    def draw(self):
        self.image.draw(self.x, self.y)


class Monster_bear:
    def __init__(self):
        self.x, self.y = 500, 120
        self.frame = 0
        self.image = load_image('Bear.png')

    def update(self):
        self.frame = (self.frame+1) % 4

    def draw(self):
        self.image.draw(self.x, self.y)


class Monster_mage:
    def __init__(self):
        self.x, self.y = 100, 95
        self.frame = 0
        self.a_frame = 0
        self.image = load_image('Mage_Attack.png')
        self.attack_image = load_image('Attack_ball.png')

    def update(self):
        self.frame = (self.frame+1) % 8
        self.a_frame = (self.a_frame+1) % 5
        delay(0.03)

    def draw(self):
        self.image.clip_draw(self.frame * 89, 0, 89, 89, self.x, self.y)
        self.attack_image.clip_draw(self.a_frame * 16, 0, 16, 9, 180 + (self.a_frame*5), 90, 40, 40)


def handle_events():
    global running
    global dir
    global dir_y
    global adjust_on
    global vector

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
                vector = 14
            elif event.key == SDLK_LEFT:
                dir -= 1
                vector = 6
            elif event.key == SDLK_x:
                work_adjust_jump()
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_p:
                game_framework.push_state(pause_state)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
                vector = 15
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

def black_HP():
    if hp_bar.damaging:
        for i in range(boy.hit_count):
            if i <= 21:
                hp_bar.damaged_image.draw(263 - i * 11, 550)


def enter():
    global boy, ground, background, hp_bar, spike, bear, mage
    boy = Boy()
    ground = Ground()
    background = Background()
    hp_bar = HP_BAR()
    spike = Spike()
    bear = Monster_bear()
    mage = Monster_mage()


def exit():
    global boy, ground, background, hp_bar, spike, bear, mage
    del boy
    del ground
    del background
    del hp_bar
    del spike, bear, mage


def pause():
    pass


def resume():
    pass


def update():
    boy.update(dir, dir_y, vector)
    bear.update()
    mage.update()
    adjust_jump()
    if (boy.x > 680 and boy.x < 720 and boy.y <= 50):
        boy.damaged(4)
    if (boy.x > 200 and boy.x < 240 and boy.y <= 50):
        boy.damaged(4)
    if (boy.x > 460 and boy.x < 500 and boy.y <= 50):
        boy.damaged(4)

    boy.game_over()
    delay(0.01)


def draw():
    global boy, ground, background, hp_bar, spike, bear, mage
    clear_canvas()
    background.draw()
    ground.draw()
    boy.draw()
    spike.draw()
    bear.draw()
    mage.draw()
    hp_bar.draw()
    black_HP()
    update_canvas()

