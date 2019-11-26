from pico2d import *
import game_framework


class Heat_box:
    def __init__(self):
        self.x, self.y = 0, 0

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10