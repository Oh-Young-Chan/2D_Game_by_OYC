from pico2d import *
import game_framework

class Health_item:
    def __init__(self):
        self.x, self.y = 300, 80
        self.image = load_image('health_item_icon.png')

    def draw(self):
        self.image.draw(self.x, self.y, 70, 70)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 35, self.y - 35, self.x + 35, self.y + 35