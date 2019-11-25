from pico2d import *
import game_framework
import game_over_state
import pause_state

from hp_bar import HP_BAR

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 13
FRAMES_PER_RUN = 8
FRAMES_PER_ATTACK = 10


RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, PRESS_X, PRESS_ATTACK, TIME_OUT, DASH = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): PRESS_X,
    (SDL_KEYDOWN, SDLK_z): PRESS_ATTACK,
    (SDL_KEYDOWN, SDLK_c): DASH
}


dir_y = 0

class IdleState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 0
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 0

    @staticmethod
    def exit(boy, event):
        global dir_y

        if event == DASH:
            if boy.dir == 1:
                boy.x += 30
            else:
                boy.x -= 30

        boy.jump_timer = 10
        dir_y = clamp(0, dir_y, 90)

    @staticmethod
    def do(boy):
        global dir_y

        boy.frame = (boy.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time * 0.2) % 13
        boy.jump_timer -= 1

        if boy.jump_timer <= 0:
            dir_y -= 10
            dir_y = clamp(0, dir_y, 90)

    @staticmethod
    def draw(boy):
        global dir_y
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 480, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 224, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)


class RunState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 0
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 0

    @staticmethod
    def exit(boy, event):
        global dir_y

        if event == DASH:
            if boy.dir == 1:
                boy.x += 30
            else:
                boy.x -= 30

        boy.jump_timer = 10
        dir_y = clamp(0, dir_y, 90)

    @staticmethod
    def do(boy):
        global dir_y

        boy.frame = (boy.frame + FRAMES_PER_RUN * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)

        boy.jump_timer -= 1

        if boy.jump_timer <= 0:
            dir_y -= 10
            dir_y = clamp(0, dir_y, 90)

    @staticmethod
    def draw(boy):
        global dir_y

        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 448, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 192, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)


class JumpState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 0
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
            boy.dir = 0

    @staticmethod
    def exit(boy, event):
        global dir_y

        if event == DASH:
            if boy.dir == 1:
                boy.x += 30
            else:
                boy.x -= 30

        boy.jump_timer = 10
        dir_y = clamp(0, dir_y, 90)

    @staticmethod
    def do(boy):
        global dir_y

        boy.frame = (boy.frame + FRAMES_PER_RUN * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        dir_y = clamp(0, dir_y, 90)

        if boy.jump_timer > 0:
            dir_y += 10
            boy.jump_timer -= 1
        elif boy.jump_timer <= 0:
            dir_y -= 10
            dir_y = clamp(0, dir_y, 90)


    @staticmethod
    def draw(boy):
        global dir_y
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 448, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 192, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)


class AttackState:
    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.dir = 0
        elif event == RIGHT_UP:
            boy.dir = 1
        elif event == LEFT_UP:
            boy.dir = 0

        boy.attack_count += 1
        print(boy.attack_count)

    @staticmethod
    def exit(boy, event):
        boy.attack_count = 0

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)

        if boy.frame > 9:
            boy.add_event(TIME_OUT)

    @staticmethod
    def draw(boy):
        global dir_y

        if boy.attack_count == 1:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 416, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 160, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
        elif boy.attack_count == 2:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 384, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 128, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
        elif boy.attack_count == 3:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 352, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 96, 32, 32, boy.x, 108 + boy.y + dir_y, 100, 100)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                PRESS_X: JumpState, PRESS_ATTACK: AttackState,
                DASH: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               PRESS_X: JumpState, PRESS_ATTACK: AttackState,
               DASH: RunState},
    JumpState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                PRESS_X: JumpState, DASH: JumpState},
    AttackState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                  LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                  PRESS_X: JumpState, TIME_OUT: IdleState,
                  PRESS_ATTACK: AttackState}
}


class Boy:
    def __init__(self):
        self.x, self.y = 400, 0
        self.image = load_image('Adventurer Sprite Sheet v1.1.png')
        self.dir = 1
        self.jump_timer = 10
        self.velocity = 0
        self.frame = 0
        self.HP = 100
        self.attack_count = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        global dir_y

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        print(dir_y)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def damaged(self, damaged):
        self.HP -= damaged

    def game_over(self):
        if self.HP <= 0:
            game_framework.change_state(game_over_state)
