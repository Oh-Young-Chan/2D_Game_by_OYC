from pico2d import *
import game_framework
import game_world
import main_state

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Pick_up_effect:
    def __init__(self, x, y, bg):
        self.bg = bg
        self.x, self.y = x, y
        self.image = load_image('image\Pickup.png')
        self.frame = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.frame >= 5:
            game_world.remove_object(self)


    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.image.clip_draw(32 * int(self.frame), 0, 32, 32, cx, cy)
