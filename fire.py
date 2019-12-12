from pico2d import *
import game_framework
import game_world
import main_state
import main_state_2
import Boy

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Fire:
    image = None

    def __init__(self, player_x, player_y, player_dir, bg):
        self.bg = bg
        self.x, self.y = player_x + 64, player_y
        self.dir = player_dir
        if Fire.image == None:
            Fire.image = load_image('image\Magic\Fire.png')
        self.frame = 0
        self.velocity = 10
        self.isFire = True
        self.boy = main_state.get_boy()
        self.bearList = main_state.get_Monster_Bear_List()

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if self.dir == 1:
            self.image.clip_draw(128 * int(self.frame), 0, 128, 128, cx, cy)
        else:
            self.image.clip_composite_draw(128 * int(self.frame), 0, 128, 128, 0, 'h', cx - 128, cy, 128, 128)


    def update(self):
        if self.boy.onFire and self.boy.fireSpellCount > 0:
            self.boy.fireSpellCount -= 1 * FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.boy.velocity = 0  # 공격 중 떼기 이동 버그 고치기, 점프시 활성화 불가
            print(self.frame)
        else:
            game_world.remove_object(self)

        for i in range(len(self.bearList)):
            if collide(self, self.bearList[i]):
                self.bearList[i].damaged(self.boy.INT * 0.5, self.isFire)

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if self.dir == 1:
            return cx - 32, cy - 12, cx + 48, cy + 12
        else:
            return cx - 128 - 48, cy - 12, cx - 128 + 32, cy + 12
