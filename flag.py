from pico2d import *
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Flag:
    def __init__(self, bg):
        self.bg = bg
        self.x, self.y = 3700, 320+28
        self.frame = 0
        self.image = load_image('image\Flag.png')

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.image.clip_draw(32*int(self.frame), 0, 32, 32, cx, cy)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        return cx-20, cy-10, cx+20, cy+10