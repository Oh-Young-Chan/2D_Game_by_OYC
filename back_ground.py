from pico2d import *
import game_framework

width = 1280 // 2
height = 720 // 2

class Background:
    def __init__(self):
        global width, height
        self.x, self.y = width, height
        self.image = load_image('image\Background.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass