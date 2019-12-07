from pico2d import *
import game_framework

class Spike:
    def __init__(self):
        self.x, self.y = 64*10+64, 64 + (64-32)
        self.image = load_image('image\spike.png')

    def draw(self):
        self.image.draw(self.x, self.y, 64, 64)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15