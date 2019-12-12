from pico2d import *
import game_framework

class Ground:
    startGround = None
    middleGround = None
    endGround = None
    bottomStartGround = None
    bottomMiddleGround = None
    bottomEndGround = None
    groundList = [(0, 1000), (1200, 2000), (2000, 3800)]

    def __init__(self, i, bg):
        self.bg = bg
        self.x1, self.x2 = self.groundList[i]
        self.y = 64 + (64-32)
        self.bottom = (64-32)
        if Ground.startGround == None:
            Ground.startGround = load_image('image\Tile\TileSet_01.png')
        if Ground.middleGround == None:
            Ground.middleGround = load_image('image\Tile\TileSet_02.png')
        if Ground.endGround == None:
            Ground.endGround = load_image('image\Tile\TileSet_03.png')

        if Ground.bottomStartGround == None:
            Ground.bottomStartGround = load_image('image\Tile\TileSet_08.png')
        if Ground.bottomMiddleGround == None:
            Ground.bottomMiddleGround = load_image('image\Tile\TileSet_09.png')
        if Ground.bottomEndGround == None:
            Ground.bottomEndGround = load_image('image\Tile\TileSet_10.png')

    def draw(self):
        cx1, cx2, cy, bottom_cy = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left,\
                                  self.y - self.bg.window_bottom, self.bottom - self.bg.window_bottom
        if (cx2 - cx1) <= 64:
            self.middleGround.draw(cx1+32, cy)
            self.bottomMiddleGround.draw(cx1+32, bottom_cy, 64, 64)
        elif 64 < (cx2 - cx1) <= 128:
            self.middleGround.draw(cx1+32, cy)
            self.bottomMiddleGround.draw(cx1 + 32, bottom_cy, 64, 64)
            self.middleGround.draw(cx2-32, cy)
            self.bottomMiddleGround.draw(cx2-32, bottom_cy, 64, 64)
        elif 128 < (cx2 - cx1) <= 192:
            self.startGround.draw(cx1+32, cy)
            self.bottomStartGround.draw(cx1 + 32, bottom_cy, 64, 64)
            self.middleGround.draw(cx1+32+(cx2-cx1-128), cy)
            self.bottomMiddleGround.draw(cx1+32+(cx2-cx1-128), bottom_cy, 64, 64)
            self.endGround.draw(cx2-32, cy)
            self.bottomEndGround.draw(cx2-32, bottom_cy, 64, 64)
        elif 192 < (cx2 - cx1):
            self.startGround.draw(cx1+32, cy)
            self.bottomStartGround.draw(cx1+32, bottom_cy, 64, 64)
            for i in range(1, (cx2 - cx1 - 128) // 64 + 1):
                self.middleGround.draw((cx1+32) + (64*i), cy)
                self.bottomMiddleGround.draw((cx1+32) + (64*i), bottom_cy, 64, 64)
            self.middleGround.draw((cx1+32) + 64*((cx2 - cx1 - 128) // 64) + (cx2 - cx1 - 128) % 64, cy)
            self.bottomMiddleGround.draw((cx1+32) + 64*((cx2 - cx1 - 128) // 64) + (cx2 - cx1 - 128) % 64 , bottom_cy, 64, 64)
            self.endGround.draw(cx2-32, cy)
            self.bottomEndGround.draw(cx2-32, bottom_cy, 64, 64)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        cx1, cx2, cy = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left, self.y - self.bg.window_bottom
        return cx1-16, cy+-20, cx2-16, cy+30