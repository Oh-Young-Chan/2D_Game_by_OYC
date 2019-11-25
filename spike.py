from pico2d import *
import game_framework

class Spike:
    def __init__(self):
        self.x, self.y = 700, 70
        self.image = load_image('spike.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass