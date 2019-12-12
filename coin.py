from pico2d import *
import game_framework
import game_world
import main_state

import pick_up_effect

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


class Coin:
    def __init__(self, chest_x, chest_y, bg):
        self.bg = bg
        self.x, self.y = chest_x - 20, chest_y + 10  # 상자 오픈 시 치킨 생성 좌표 조정
        self.image = load_image('image\Item\Coin.png')
        self.frame = 0
        self.fall_speed = 100
        self.boy = main_state.get_boy()
        self.ground = main_state.get_ground()
        self.flatform = main_state.get_flatform()

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.image.clip_draw(32*int(self.frame), 0, 32, 32, cx, cy, 48, 48)         # 24, 24 : 코인 크기


    def stop(self):
        self.fall_speed = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

        if collide(self, self.ground[0]) or collide(self, self.ground[1]) or collide(self, self.ground[4]) or collide(self, self.ground[6]): # 모든 땅에 작용하게 하기
            self.stop()
            if collide(self, self.boy):
                self.pickUpEffect = pick_up_effect.Pick_up_effect(self.x, self.y, self.bg)
                game_world.add_object(self.pickUpEffect, 2)
                self.boy.coinCount += 1
                game_world.remove_object(self)
                self.y -= 1000

        self.y -= self.fall_speed * game_framework.frame_time

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        return cx - 12, cy - 12, cx + 12, cy + 12