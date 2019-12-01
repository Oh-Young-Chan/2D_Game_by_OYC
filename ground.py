from pico2d import *
import game_framework

class Ground:
    def __init__(self):
        self.x, self.y = 0, 30
        self.image_start = load_image('ground1x1.png')
        self.image_middle = load_image('ground1x2.png')

    def draw(self):
        self.image_start.draw(0, self.y)
        for i in range(0, 11+1):
            self.image_middle.draw(64 + 64 * i, self.y)

        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 1600-1, 60