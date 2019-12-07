from pico2d import *
import game_framework

class Ground:
    def __init__(self):
        self.x, self.y = 0, 64 + (64-32)
        self.image_start = load_image('image\TileSet_01.png')
        self.image_middle = load_image('image\TileSet_02.png')
        self.image_end = load_image('image\TileSet_03.png')

    def draw(self):
        self.image_start.draw(0, self.y)                # 0
        for i in range(0, 9):                           # 1~9
            self.image_middle.draw(64 + 64 * i, self.y)
        self.image_end.draw(640, self.y)                # 10

        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 1280-1, 64*2