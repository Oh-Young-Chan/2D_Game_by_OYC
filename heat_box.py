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
    def __init__(self):
        boy = main_state.get_boy()
        self.x, self.y = boy.x + 30, boy.y
        self.attack_time = 1
        self.isFire = False

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        Monster_Bear_List = main_state.get_Monster_Bear_List()
        Monster_Mage_List = main_state.get_Monster_Mage_List()
        boy = main_state.get_boy()

        self.attack_time -= 1
        self.attack_time = clamp(0, self.attack_time, 1)
        if self.attack_time == 0:
            pass
        else:
            self.attack_time = 1

        for i in range(len(Monster_Bear_List)):
            if collide(self, Monster_Bear_List[i]):
                game_world.remove_object(self)
                Monster_Bear_List[i].damaged(boy.STR, self.isFire)
        for i in range(len(Monster_Mage_List)):
            if collide(self, Monster_Mage_List[i]):
                Monster_Mage_List[i].damaged(boy.STR, self.isFire)

    def get_bb(self):
        boy = main_state.get_boy()

        if boy.dir == 1:
            return self.x, self.y - 50, self.x + 20, self.y + 10
        else:
            return self.x - 60, self.y - 50, self.x - 80, self.y + 10