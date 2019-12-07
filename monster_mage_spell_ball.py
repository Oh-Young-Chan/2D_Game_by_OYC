from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_ATTACK_ACTION = 5

class Monster_mage_spell_ball:
    def __init__(self):
        self.image = load_image('image\Attack_ball.png')

    def update(self):
        pass

    def draw(self):
        pass