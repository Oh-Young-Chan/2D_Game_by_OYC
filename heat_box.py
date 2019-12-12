from pico2d import *
import game_framework
import game_world

import main_state


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

class Heat_box:
    def __init__(self, bg):
        self.bg = bg
        self.boy = main_state.get_boy()
        self.x, self.y = self.boy.x + 30, self.boy.y
        self.attack_time = 1
        self.isFire = False
        self.timer = 0.001

    def draw(self):
        pass

    def update(self):
        Monster_Bear_List = main_state.get_Monster_Bear_List()
        Monster_Mage_List = main_state.get_Monster_Mage_List()

        self.attack_time -= 1
        self.attack_time = clamp(0, self.attack_time, 1)
        if self.attack_time == 0:
            pass
        else:
            self.attack_time = 1

        for i in range(len(Monster_Bear_List)):
            if collide(self, Monster_Bear_List[i]):
                game_world.remove_object(self)
                Monster_Bear_List[i].damaged(self.boy.STR, self.isFire)
        for i in range(len(Monster_Mage_List)):
            if collide(self, Monster_Mage_List[i]):
                game_world.remove_object(self)
                Monster_Mage_List[i].damaged(self.boy.STR, self.isFire)

        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 0.001
            game_world.remove_object(self)

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        if self.boy.dir == 1:
            return cx + 30, cy - 30, cx + 50, cy + 30
        else:
            return cx - 80, cy - 30, cx - 60, cy + 30