from pico2d import *
import game_framework

class Ground:
    startGround = None
    middleGround = None
    endGround = None
    bottomStartGround = None
    bottomMiddleGround = None
    bottomEndGround = None
    groundList = [(0, 800), (800, 1000), (1200, 2000), (2000, 3200), (0, 1000), (3300, 3858), (1050, 2010)]
    groundYList = [(0, 360+64*2-32), (0, 360+64*5-32), (0, 360+64*2-32), (0, 360+64*10-16), (360+64*11, 360+64*13-32),
                    (0, 300), (360+64*7, 360+64*8)]

    def __init__(self, i, bg):
        self.bg = bg
        self.x1, self.x2 = self.groundList[i]
        self.y1, self.y2 = self.groundYList[i]
        #self.y = 64 + (64-32)
        #self.bottom = (64-32)
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
        cx1, cx2, cy1, cy2 = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left,\
                                self.y1 - self.bg.window_bottom, self.y2 - self.bg.window_bottom
                                  #self.y - self.bg.window_bottom, self.bottom - self.bg.window_bottom

        if 192 < (cx2 - cx1):
            self.startGround.draw(cx1+32, cy2)
            for i in range(1, (cx2 - cx1 - 128) // 64 + 1):
                self.middleGround.draw((cx1+32) + (64*i), cy2)
            self.middleGround.draw((cx1+32) + 64*((cx2 - cx1 - 128) // 64) + (cx2 - cx1 - 128) % 64, cy2)
            self.endGround.draw(cx2-32, cy2)

        if 64 <= cy2-cy1:
            for i in range(0, (cy2-cy1)//64+1):
                self.bottomStartGround.draw(cx1 + 32, cy2-32-i*64, 64, 64)
                self.bottomEndGround.draw(cx2 - 32, cy2-32-i*64, 64, 64)
                self.bottomMiddleGround.draw((cx1 + 32) + 64 * ((cx2 - cx1 - 128) // 64) + (cx2 - cx1 - 128) % 64,
                                             cy2-32-i*64, 64, 64)
            for i in range(1, (cx2 - cx1 - 128) // 64 + 1):
                for j in range(0, (cy2 - cy1) // 64 + 1):
                    self.bottomMiddleGround.draw((cx1+32) + (64*i), cy2-32-j*64, 64, 64)

    def update(self):
        pass

    def get_bb(self):
        cx1, cx2, cy1, cy2 = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left,\
                             self.y1 - self.bg.window_bottom, self.y2 - self.bg.window_bottom
        return cx1, cy1+-20, cx2, cy2+30