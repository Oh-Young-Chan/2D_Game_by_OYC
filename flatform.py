from pico2d import *
import game_framework

class Flatform:
    def __init__(self):
        self.x, self.y = 200, 200

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x-50, self.y-1, self.x+50, self.y+1