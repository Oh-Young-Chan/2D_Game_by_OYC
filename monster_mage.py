from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_ATTACK_ACTION = 5

class Monster_mage:
    def __init__(self):
        self.x, self.y = 100, 95
        self.HP = 80
        self.frame = 0
        self.a_frame = 0
        self.image = load_image('Mage_Attack.png')
        self.attack_image = load_image('Attack_ball.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.a_frame = (self.a_frame + FRAMES_PER_ATTACK_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

        if self.HP <= 0:
            game_world.remove_object(self)
            self.y -= 1000

    def draw(self):
        self.image.clip_draw(int(self.frame) * 89, 0, 89, 89, self.x, self.y)
        self.attack_image.clip_draw(int(self.a_frame) * 16, 0, 16, 9, 180 + (self.a_frame*5), 90, 40, 40)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 35, self.x + 30, self.y + 45

    def damaged(self, damage):
        self.HP -= damage
        print(self.HP)