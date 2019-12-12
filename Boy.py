from pico2d import *
import game_framework
import game_world
import game_over_state
import pause_state
import main_state

from hp_bar import HP_BAR
from heat_box import Heat_box
from ground import Ground
from lightning import Lightning
from fire import Fire

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
FRAMES_PER_IDLE = 4
FRAMES_PER_RUN = 6
FRAMES_PER_JUMP = 8
FRAMES_PER_ATTACK = 4
FRAMES_PER_HURT = 4
FRAMES_PER_FIRE = 4

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, PRESS_Z, END_ACT= range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    #(SDL_KEYDOWN, SDLK_x): PRESS_X,
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

        #if event == PRESS_Z:
         #   boy.act_attack()

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        global width, height

        boy.frame = (boy.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 4
        boy.x += boy.velocity * game_framework.frame_time
        #boy.x = clamp(25, boy.x, 1280 - 25)
        boy.x = clamp(0, boy.x, boy.bg.w)

        #if boy.jump_timer > 0:  # 공중에서 키보드 입력으로 Idle 상태로 바뀌어도 상승과 낙하를 유지해준다.
         #   boy.y += 20
          #  boy.jump_timer -= 1
           # boy.y = clamp(108, boy.y, 700)
            #boy.fall_speed = 0
            #boy.jumping = True
        #else:
         #   boy.jumping = False

        if boy.dash_timer != 0:
            boy.dash_timer -= 1
            boy.dash_timer = clamp(0, boy.dash_timer, 10)
            boy.y = clamp(boy.y, boy.y, 700)

    @staticmethod
    def draw(boy):
        cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom # 현재 캔버스에서 드로우 좌표
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame) * 32, 0, 32, 32, cx, cy, 64, 64)
        else:
            boy.image.clip_composite_draw(int(boy.frame) * 32, 0, 32, 32, 0, 'h', cx, cy, 64, 64)
        if boy.dash_timer != 0:
            if boy.dir == 1:
                boy.image_dash.clip_composite_draw(0, 0, 32, 32, 0, '', cx - 60, cy - 15, 100, 30)
            else:
                boy.image_dash.clip_composite_draw(0, 0, 32, 32, 0, 'v', cx + 60, cy - 15, 100, 30)


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
            if boy.velocity == 0:
                pass
            else:
                boy.velocity -= RUN_SPEED_PPS
            boy.dir = 1
        elif event == LEFT_UP:
            if boy.velocity == 0:
                pass
            else:
                boy.velocity += RUN_SPEED_PPS
            boy.dir = 0

        #if event == PRESS_Z:
         #   boy.act_attack()

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        global width, height

        boy.frame = (boy.frame + FRAMES_PER_RUN * ACTION_PER_TIME * game_framework.frame_time) % 6
        boy.x += boy.velocity * game_framework.frame_time
        #boy.x = clamp(25, boy.x, 1280 - 25)
        boy.x = clamp(0, boy.x, boy.bg.w)

        #if boy.jump_timer > 0:  # 공중에서 키보드 입력으로 Run 상태로 바뀌어도 상승과 낙하를 유지해준다.
         #   boy.y += 20
          #  boy.jump_timer -= 1
           # boy.y = clamp(108, boy.y, 700)
            #boy.fall_speed = 0
            #boy.jumping = True
        #else:
         #   boy.jumping = False

        if boy.dash_timer != 0:
            boy.dash_timer -= 1
            boy.dash_timer = clamp(0, boy.dash_timer, 10)
            boy.y = clamp(boy.y, boy.y, 700)

    @staticmethod
    def draw(boy):
        cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom # 현재 캔버스에서 드로우 좌표
        if boy.dir == 1:
            boy.runImage.clip_draw(int(boy.frame) * 32, 0, 32, 32, cx, cy, 64, 64)
        else:
            boy.runImage.clip_composite_draw(int(boy.frame) * 32, 0, 32, 32, 0, 'h', cx, cy, 64, 64)
        if boy.dash_timer != 0:
            if boy.dir == 1:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, '', cx - 60, cy - 15, 100, 30)
            else:
                boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, 'v', cx + 60, cy - 15, 100, 30)


#class JumpState:
 #   @staticmethod
  #  def enter(boy, event):
   #     if event == RIGHT_DOWN:
    #        boy.velocity += RUN_SPEED_PPS
     #       boy.dir = 1
      #  elif event == LEFT_DOWN:
       #     boy.velocity -= RUN_SPEED_PPS
        #    boy.dir = 0
        #elif event == RIGHT_UP:
         #   boy.velocity -= RUN_SPEED_PPS
          #  boy.dir = 1
        #elif event == LEFT_UP:
         #   boy.velocity += RUN_SPEED_PPS
          #  boy.dir = 0

        #if event == PRESS_Z:
         #   boy.act_attack()

        #boy.y += 5  # 충돌로 인한 점프불가를 방지하기 위한 눈치못챌정도의 작은 점프
        #boy.jump_timer = 10

    #@staticmethod
    #def exit(boy, event):
     #   # boy.jump_timer_other = boy.jump_timer  # 공중에서 키보드 입력으로 Idle 상태로 바뀌어도 상승과 낙하를 유지해준다.

      #  boy.jump_timer = 0

    #@staticmethod
    #def do(boy):
     #   global width, height

      #  boy.frame = (boy.frame + FRAMES_PER_JUMP * ACTION_PER_TIME * game_framework.frame_time) % 8
       # boy.x += boy.velocity * game_framework.frame_time
        ###boy.x = clamp(25, boy.x, 1280 - 25)
        #boy.x = clamp(0, boy.x, boy.bg.w)

        #if boy.jump_timer > 0:
         #   boy.y += 5
          #  boy.jump_timer -= 1
           # boy.y = clamp(108, boy.y, 700)
            #boy.fall_speed = 0
           # boy.jumping = True
        #else:
         #   boy.jumping = False

        #if boy.dash_timer != 0:
         #   boy.dash_timer -= 1
          #  boy.dash_timer = clamp(0, boy.dash_timer, 10)
           # boy.y = clamp(boy.y, boy.y, 700)

   # @staticmethod
    #def draw(boy):
     #   cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom # 현재 캔버스에서 드로우 좌표
      #  if boy.dir == 1:
       #     boy.jumpImage.clip_draw(int(boy.frame) * 32, 0, 32, 32, cx, cy, 64, 64)
        #else:
         #   boy.jumpImage.clip_composite_draw(int(boy.frame) * 32, 0, 32, 32, 0, 'h', cx, cy, 64, 64)
        #if boy.dash_timer != 0:
         #   if boy.dir == 1:
          #      boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, '', cx - 60, cy - 15, 100, 30)
           # else:
            #    boy.image_dash.clip_composite_draw(0, 0, 415, 81, 0, 'v', cx + 60, cy - 15, 100, 30)


class AttackState:
    @staticmethod
    def enter(boy, event):
        #print('AttackState')
        pass

    @staticmethod
    def exit(boy, event):
        boy.attackFrame = 0
        boy.velocity = 0
        #print('End')

    @staticmethod
    def do(boy):
        boy.x = clamp(0, boy.x, boy.bg.w)
        boy.attackFrame = (boy.attackFrame + FRAMES_PER_ATTACK * ACTION_PER_TIME * game_framework.frame_time) % (4+1)
        if boy.attackFrame >= 4:
            boy.add_event(END_ACT)
        elif boy.attackFrame >= 2:
            boy.act_attack()
        else:
            pass

    @staticmethod
    def draw(boy):
        cx, cy = boy.x - boy.bg.window_left, boy.y - boy.bg.window_bottom # 현재 캔버스에서 드로우 좌표
        if boy.dir == 1:
            boy.attackImage.clip_draw(32*int(boy.attackFrame), 0, 32, 32, cx, cy, 64, 64)
        else:
            boy.attackImage.clip_composite_draw(32*int(boy.attackFrame), 0, 32, 32, 0, 'h', cx, cy, 64, 64)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                PRESS_Z: AttackState,
                END_ACT: IdleState},  # TIME_OUT: IdleState 추가해야 공격할 때 다른 버튼 연타해도 안 튕김
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               PRESS_Z: AttackState,
               END_ACT: IdleState},
    AttackState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                  LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
                  PRESS_Z: AttackState,
                  END_ACT: IdleState}
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
    def __init__(self, bg):
        self.bg = bg
        #self.x, self.y = 64 * 6, 64 * 2 + 32  # 32 = 플레이어 높이 // 2
        self.x = 64 * 6  # 전체 백그라운드 중에서 드로우 좌표
        self.y = 360+64 * 3+32  # 전체 백그라운드 중에서 드로우 좌표
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.image = load_image('image\Player\Idle.png')
        self.runImage = load_image('image\Player\Run.png')
        self.jumpImage = load_image('image\Player\Jump.png')
        self.attackImage = load_image('image\Player\Attack.png')
        self.image_dash = load_image('image\dash_effect.png')
        self.hurtImage = load_image('image\Player\Hurt.png')
        self.dir = 1
        self.jump_timer = 0.1
        self.jumped = False
        self.workingJump = True
        self.stop_jump_while_dash = 0
        self.dash_timer = 0
        self.velocity = 0
        self.velocityOnY = 0
        self.fall_speed = 400
        self.jumping = False
        self.frame = 0
        self.attackFrame = 0
        self.hurtFrame = 0
        self.hurting = False
        self.invincibilityTime = 10
        self.HP = 100
        self.STR = 30
        self.INT = 50
        self.attack_count = 0
        self.coinCount = 0
        self.groundList = Ground.groundList
        self.groundYList = Ground.groundYList
        self.ax = 0
        self.bx = 0
        self.ay = 0
        self.by = 0
        self.ground0 = Ground(0, self.bg)
        self.ground1 = Ground(1, self.bg)
        self.ground2 = Ground(2, self.bg)
        self.ground3 = Ground(3, self.bg)
        self.ground4 = Ground(4, self.bg)
        self.ground5 = Ground(5, self.bg)
        self.ground6 = Ground(6, self.bg)
        self.chicken = None
        self.inCure = False
        self.onFire = False
        self.onFlatform = False
        self.potionHealthy = 40
        self.itemList = [[], [], []]  # Item
        self.magicList = [[], [], []]  # Magic
        self.fireSpellCount = 0
        self.light = None
        self.fire = None
        self.font = load_font('ConsolaMalgun.ttf')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


    def set_background(self, bg):
        self.bg = bg


    #boy.canvas_width // 2, boy.y
    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom  # 현재 캔버스에서 드로우 좌표
        return cx - 20, cy - 32, cx + 18, cy + 24

    def get_flatform_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom  # 현재 캔버스에서 드로우 좌표
        return cx - 20, cy - 32, cx + 18, cy - 24

    def onJump(self):
        self.fall_speed = 0
        self.jumped = True
        self.workingJump = False

    def workJump(self):
        pass

    def funcjumping(self):
        if self.jumped:
            if self.jump_timer >= 0:
                if self.workingJump:
                    self.y += 1000*game_framework.frame_time
                else:
                    pass

    def drinkPotion(self):
        if len(self.itemList[0]) <= 0 or self.HP >= 100:
            pass
        else:
            self.itemList[0].pop(-1)
            self.recovery(self.potionHealthy)

    def spellLight(self):
        if len(self.magicList[0]) <= 0:
            pass
        else:
            self.magicList[0].pop(-1)
            self.light = Lightning(self.x, self.y, self.dir, self.bg)
            game_world.add_object(self.light, 1)


    def spellOnFire(self):
        self.onFire = True
        self.fire = Fire(self.x, self.y, self.dir, self.bg)


    def spellOffFire(self):
        self.onFire = False

    def spellFire(self):
        if self.fireSpellCount > 0 and self.onFire:
            if game_framework.frame_count % 15 == 0:
                game_world.add_object(self.fire, 1)
        elif self.onFire == False:
            pass

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
        Heat_Box = Heat_box(self.bg)
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

    def pop_event(self):
        self.event_que.pop(-1)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0 and (self.attackFrame == 0 or self.attackFrame >= 4):
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        elif len(self.event_que) > 0:
            self.event_que.pop()

        if self.jumping:  # 상태의 do에 있는 fall_speed 값 조정과의 충돌을 피하기 위함
            pass
        else:
            if self.onFlatform: # 플랫폼 밟고 있으면
                self.fall_speed = 0
            else:
                if self.jumped: # 점프 했으면
                    if self.workingJump:
                        self.fall_speed = 0
                    else:
                        self.fall_speed = 400
                else:
                    self.fall_speed = 400

        if collide(self, self.ground0): # 스테이지1 미적용 시키고 스테이지2도 추개하주기
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground1):
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground2):
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground3):
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground4):
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground5):
            self.stop()
            self.x_stop()
            self.workingJump = True
        if collide(self, self.ground6):
            self.stop()
            self.x_stop()
            self.workingJump = True

        self.inficovery()
        self.spellFire()

        if self.jumped:
            self.jump_timer -= game_framework.frame_time
            if self.jump_timer < 0:
                self.jumped = False
                self.workingJump = True
                self.jump_timer = 0.1

        self.funcjumping()

        self.y -= self.fall_speed * game_framework.frame_time
        self.HP = clamp(0, self.HP, 100)

        if self.hurting:
            self.hurtFrame += (self.hurtFrame + FRAMES_PER_HURT * ACTION_PER_TIME * game_framework.frame_time) % (4+1)
            if self.hurtFrame >= 4:
                self.hurting = False
                self.hurtFrame = 0


    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom  # 현재 캔버스에서 드로우 좌표
        if self.hurting:
            self.hurtImage.clip_draw(32*int(self.hurtFrame), 0, 32, 32, cx, cy, 64, 64)
        else:
            self.cur_state.draw(self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def damaged(self, damage):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom  # 현재 캔버스에서 드로우 좌표
        self.hurting = True
        if 0 < self.hurtFrame <= 3:
            self.HP -= damage
            if self.dir == 1:
                self.x -= cx * FRAMES_PER_HURT * ACTION_PER_TIME * game_framework.frame_time
            else:
                self.x += cx * FRAMES_PER_HURT * ACTION_PER_TIME * game_framework.frame_time

    def recovery(self, cure):
        self.HP += cure

    def dotRecovery(self, cure):
        self.HP += cure * game_framework.frame_time * 0.05

    def inficovery(self):
        if game_framework.frame_count % 2 == 0:
            self.infinityCure()

    def stop(self):
        self.fall_speed = 0

    def x_stop(self):
        pass

    def flatform_stop(self):
        self.onFlatform = True

