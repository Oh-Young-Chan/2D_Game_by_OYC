from pico2d import *
import game_framework

class Monster_bear:
    def __init__(self):
        self.x, self.y = 500, 120
        self.frame = 0
        self.image = load_image('Bear.png')

    def update(self):
        self.frame = (self.frame+1) % 4

    def draw(self):
        self.image.draw(self.x, self.y)