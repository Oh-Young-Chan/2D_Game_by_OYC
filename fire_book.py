from pico2d import *
import game_framework
import game_world
import main_state

import pick_up_effect

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Fire_Book:
    def __init__(self, chest_x, chest_y, bg):
        self.bg = bg
        self.x, self.y = chest_x+70, chest_y+40                 # 상자 오픈 시 치킨 생성 좌표 조정
        self.image = load_image('image\Item\Fire_Book.png')
        self.fall_speed = 100
        self.boy = main_state.get_boy()
        self.ground = main_state.get_ground()

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.image.draw(cx, cy, 24, 24)         # 24, 24 : 치킨 크기


    def stop(self):
        self.fall_speed = 0

    def update(self):
        if collide(self, self.ground[0]) or collide(self, self.ground[1]) or collide(self, self.ground[4]) or collide(self, self.ground[6]): # 모든 땅에 작용하게 하기
            self.stop()
            if collide(self, self.boy):
                self.pickUpEffect = pick_up_effect.Pick_up_effect(self.x, self.y, self.bg)
                game_world.add_object(self.pickUpEffect, 2)
                self.boy.fireSpellCount += 100
                game_world.remove_object(self)
                self.y -= 1000

        self.y -= self.fall_speed * game_framework.frame_time

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        return cx - 12, cy - 12, cx + 12, cy + 12