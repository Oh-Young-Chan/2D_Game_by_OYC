from pico2d import *
import game_framework
import game_world
import main_state

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

    def __init__(self, player_x, player_y, player_dir):
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
        if self.dir == 1:
            self.image.clip_draw(128 * int(self.frame), 0, 128, 128, self.x, self.y)
        else:
            self.image.clip_composite_draw(128 * int(self.frame), 0, 128, 128, 0, 'h', self.x - 128, self.y, 128, 128)
        draw_rectangle(*self.get_bb())

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
                self.bearList[i].damaged(self.boy.INT * 0.2, self.isFire)

    def get_bb(self):
        if self.dir == 1:
            return self.x - 32, self.y - 12, self.x + 48, self.y + 12
        else:
            return self.x - 128 - 48, self.y - 12, self.x - 128 + 32, self.y + 12
