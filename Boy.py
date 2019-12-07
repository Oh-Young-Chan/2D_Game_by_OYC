from pico2d import *
import game_framework
import game_world
import game_over_state
import pause_state
import main_state

from hp_bar import HP_BAR
from heat_box import Heat_box
from ground import Ground

width = 1280 // 2
height = 720 // 2

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

DASH_SPEED_KMPH = 60.0
DASH_SPEED_MPM = (DASH_SPEED_KMPH * 1000.0 / 60.0)
DASH_SPEED_MPS = (DASH_SPEED_MPM / 60.0)
DASH_SPEED_PPS = (DASH_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 13
FRAMES_PER_RUN = 8
FRAMES_PER_ATTACK = 10

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, PRESS_X, PRESS_Z = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): PRESS_X,
    (SDL_KEYDOWN, SDLK_z): PRESS_Z
}


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

        if event == PRESS_Z:
            boy.act_attack()

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        global width, height

        boy.frame = (boy.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time * 0.2) % 13
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1280 - 25)

        if boy.jump_timer > 0:                      # 공중에서 키보드 입력으로 Idle 상태로 바뀌어도 상승과 낙하를 유지해준다.
            boy.y += 20
            boy.jump_timer -= 1
            boy.y = clamp(108, boy.y, 500)
            boy.fall_speed = 0
            boy.jumping = True
        else:
            boy.jumping = False

        if boy.dash_timer != 0:
            boy.dash_timer -= 1
            boy.dash_timer = clamp(0, boy.dash_timer, 10)
            boy.y = clamp(boy.y, boy.y, 500)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 480, 32, 32, boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 224, 32, 32, boy.x, boy.y, 100, 100)
        if boy.dash_timer != 0:
            if boy.dir == 1:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, '', boy.x - 60, boy.y - 15, 100, 30)
            else:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, 'v', boy.x + 60, boy.y - 15, 100, 30)


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

        if event == PRESS_Z:
            boy.act_attack()

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        global width, height

        boy.frame = (boy.frame + FRAMES_PER_RUN * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1280 - 25)

        if boy.jump_timer > 0:                      # 공중에서 키보드 입력으로 Run 상태로 바뀌어도 상승과 낙하를 유지해준다.
            boy.y += 20
            boy.jump_timer -= 1
            boy.y = clamp(108, boy.y, 500)
            boy.fall_speed = 0
            boy.jumping = True
        else:
            boy.jumping = False

        if boy.dash_timer != 0:
            boy.dash_timer -= 1
            boy.dash_timer = clamp(0, boy.dash_timer, 10)
            boy.y = clamp(boy.y, boy.y, 500)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 448, 32, 32, boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 192, 32, 32, boy.x, boy.y, 100, 100)
        if boy.dash_timer != 0:
            if boy.dir == 1:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, '', boy.x - 60, boy.y - 15, 100, 30)
            else:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, 'v', boy.x + 60, boy.y - 15, 100, 30)


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

        if event == PRESS_Z:
            boy.act_attack()

        boy.y += 5                  #충돌로 인한 점프불가를 방지하기 위한 눈치못챌정도의 작은 점프
        boy.jump_timer = 10

    @staticmethod
    def exit(boy, event):
        #boy.jump_timer_other = boy.jump_timer  # 공중에서 키보드 입력으로 Idle 상태로 바뀌어도 상승과 낙하를 유지해준다.

        boy.jump_timer = 0


    @staticmethod
    def do(boy):
        global width, height

        boy.frame = (boy.frame + FRAMES_PER_RUN * ACTION_PER_TIME * game_framework.frame_time) % 8
        boy.x += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1280 - 25)

        if boy.jump_timer > 0:
            boy.y += 20
            boy.jump_timer -= 1
            boy.y = clamp(108, boy.y, 500)
            boy.fall_speed = 0
            boy.jumping = True
        else:
            boy.jumping = False

        if boy.dash_timer != 0:
            boy.dash_timer -= 1
            boy.dash_timer = clamp(0, boy.dash_timer, 10)
            boy.y = clamp(boy.y, boy.y, 500)

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 448, 32, 32, boy.x, boy.y, 100, 100)
        else:
            boy.image.clip_draw(int(boy.frame) * 32, 192, 32, 32, boy.x, boy.y, 100, 100)
        if boy.dash_timer != 0:
            if boy.dir == 1:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, '', boy.x - 60, boy.y - 15, 100, 30)
            else:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, 'v', boy.x + 60, boy.y - 15, 100, 30)


class AttackState:
    @staticmethod
    def enter(boy, event):
        boy.attack_count += 1

    @staticmethod
    def exit(boy, event):
        if boy.attack_count >= 3:
            boy.attack_count = 0

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % 10

    @staticmethod
    def draw(boy):
        if boy.attack_count == 1:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 416, 32, 32, boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 160, 32, 32, boy.x, boy.y, 100, 100)
        elif boy.attack_count == 2:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 384, 32, 32, boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 128, 32, 32, boy.x, boy.y, 100, 100)
        else:
            if boy.dir == 1:
                boy.image.clip_draw(int(boy.frame) * 32, 352, 32, 32, boy.x, boy.y, 100, 100)
            else:
                boy.image.clip_draw(int(boy.frame) * 32, 96, 32, 32, boy.x, boy.y, 100, 100)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                PRESS_X: JumpState, PRESS_Z: IdleState},  # TIME_OUT: IdleState 추가해야 공격할 때 다른 버튼 연타해도 안 튕김
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               PRESS_X: JumpState, PRESS_Z: RunState},
    JumpState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                PRESS_X: JumpState, PRESS_Z: JumpState}
}


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Boy:
    def __init__(self):
        self.x, self.y = 64*6, 64*2+48                                      # 48 = 플레이어 높이 // 2(?)
        self.image = load_image('image\Adventurer Sprite Sheet v1.1.png')
        self.image_dash = load_image('image\dash_effect.png')
        self.dir = 1
        self.jump_timer = 0
        self.jump_timer_other = 0
        self.stop_jump_while_dash = 0
        self.dash_timer = 0
        self.velocity = 0
        self.fall_speed = 400
        self.jumping = False
        self.frame = 0
        self.HP = 100
        self.STR = 10
        self.attack_count = 0
        self.ground = Ground()
        self.chicken = None
        self.inCure = False
        self.itemList = [[], [], []]                 # Item
        self.magicList = [[], [], []]                # Magic
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def get_bb(self):
        if self.dir == 1:
            return self.x - 35, self.y - 50, self.x + 25, self.y + 20
        else:
            return self.x - 25, self.y - 50, self.x + 35, self.y + 20

    def get_flatform_bb(self):
        if self.dir == 1:
            return self.x - 35, self.y - 50, self.x + 25, self.y - 40
        else:
            return self.x - 25, self.y - 50, self.x + 35, self.y - 40


    def eatChicken(self):
        if len(self.itemList[0]) <= 0 or self.HP >= 100:
            pass
        else:
            self.itemList[0].pop(-1)
            self.recovery(50)

    def infinityCure(self):
        num = 1000
        if self.inCure:
            while num > 0:
                self.dotRecovery(1)
                num -= 1
                print('heal!')
                if self.inCure:
                    pass
                else:
                    print('break')
                    break

    def openCure(self):
        self.inCure = True

    def closeCure(self):
        self.inCure = False


    def act_attack(self):
        Heat_Box = Heat_box()
        game_world.add_object(Heat_Box, 1)

    def act_dash(self):
        if self.dir == 1:
            self.velocity += DASH_SPEED_PPS
            self.x += self.velocity * game_framework.frame_time * 5
            self.velocity -= DASH_SPEED_PPS
        else:
            self.velocity -= DASH_SPEED_PPS
            self.x += self.velocity * game_framework.frame_time * 5
            self.velocity += DASH_SPEED_PPS

        self.dash_timer += 10
        self.jump_timer = 0

    def return_boy(self):
        return self.x, self.y

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        if self.jumping:                            #상태의 do에 있는 fall_speed 값 조정과의 충돌을 피하기 위함
            pass
        else:
            self.fall_speed = 400

        if collide(self, self.ground):
            self.stop()

        self.inficovery()

        self.y -= self.fall_speed * game_framework.frame_time
        self.HP = clamp(0, self.HP, 100)


    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_flatform_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def damaged(self, damage):
        self.HP -= damage

    def recovery(self, cure):
        self.HP += cure

    def dotRecovery(self, cure):
        self.HP += cure * game_framework.frame_time * 0.05

    def inficovery(self):
        if game_framework.frame_count % 2 == 0:
            print(game_framework.frame_count)
            self.infinityCure()

    def stop(self):
        self.fall_speed = 0