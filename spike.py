from pico2d import *
import game_framework

class Spike:
    spikeImage = None
    spikeList = [(1050, 360+64*3+16), (64*19+32, 360+64*2+32), (64*20+32, 360+64*2+32), (64*21+32, 360+64*2+32),
                 (64*22+32, 360+64*2+32), (64*23+32, 360+64*2+32), (64*24+32, 360+64*2+32), (64*25+32, 360+64*2+32),
                 (64*26+32, 360+64*2+32), (64*27+32, 360+64*2+32), (64*28+32, 360+64*2+32), (64*29+32, 360+64*2+32),
                 (64*30+32, 360+64*2+32),
                 (3400-64-32, 360+64*9-8), (3220+64*5-16, 360+64*7-24), (3220+64*4+16, 600-24), (3234, 450-12)]

    def __init__(self, i, bg):
        self.bg = bg
        self.x, self.y = self.spikeList[i]
        if Spike.spikeImage == None:
            Spike.spikeImage = load_image('image\spike.png')

    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.spikeImage.draw(cx, cy, 64, 64)


    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        return cx - 15, cy - 15, cx + 15, cy + 15