from pico2d import *
import game_framework

class Background:
    def __init__(self):
        self.x, self.y = 400, 300
        self.image = load_image('back.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass