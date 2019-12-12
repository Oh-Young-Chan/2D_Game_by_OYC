from pico2d import *
import game_framework
import game_world
import main_state


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


class Flatform:
    startFlatForm = None
    middleFlatForm = None
    endFlatForm = None
    flatFormList = [(500, 550, 360+200), (550, 600, 360+280), (500, 550, 360+360), (550, 600, 360+440), (650, 700, 360+440),
                    (950, 1000, 360+64*6), (1020, 1070, 360+64*7), (1020, 1100, 360+64*2+32),
                    (1100, 1150, 360+64*9), (1150, 1200, 360+64*10), (1100, 1150, 360+64*11), (1050, 1100, 360+64*12),
                    (3220, 3220+64, 950), (3220+64*1, 3220+64*2, 880), (3220+64*3, 3220+64*4, 810), (3220+64*5-32, 3220+64*6-32, 740),
                    (3220+64*7-32, 3220+64*8-32, 670), (3220+64*6-32, 3220+64*7-32, 600), (3220+64*4, 3220+64*5, 530), (3220+64*2, 3220+64*3, 460),
                    (3220, 3220+64, 390), (1950, 2000, 360+64*9), (1950, 2000, 360+64*10)]

    def __init__(self, i, bg):
        self.x1, self.x2, self.y = self.flatFormList[i]
        self.bg = bg
        if Flatform.startFlatForm == None:
            Flatform.startFlatForm = load_image('image\Tile\FlatForm_01.png')
        if Flatform.middleFlatForm == None:
            Flatform.middleFlatForm = load_image('image\Tile\FlatForm_02.png')
        if Flatform.endFlatForm == None:
            Flatform.endFlatForm = load_image('image\Tile\FlatForm_03.png')

    def draw(self):
        cx1, cx2, cy = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left, self.y - self.bg.window_bottom
        if (cx2-cx1) <= 32:
            self.middleFlatForm.draw(cx1, cy)
        elif 32 < (cx2-cx1) <= 64:
            self.middleFlatForm.draw(cx1, cy)
            self.middleFlatForm.draw(cx2-32, cy)
        elif 64 < (cx2-cx1) <= 96:
            self.middleFlatForm.draw(cx1, cy)
            self.middleFlatForm.draw(cx1+32, cy)
            self.middleFlatForm.draw(cx2-32, cy)
        elif 96 < (cx2-cx1):
            self.startFlatForm.draw(cx1, cy)
            for i in range(1, (cx2-cx1-64)//32 + 1):
                self.middleFlatForm.draw(cx1+32*i, cy)
            self.middleFlatForm.draw(cx1+32*((cx2-cx1-64)//32) + (cx2-cx1-64)%32, cy)
            self.endFlatForm.draw(cx2-32, cy)

    def update(self):
        pass

    def get_bb(self):
        cx1, cx2, cy = self.x1 - self.bg.window_left, self.x2 - self.bg.window_left, self.y - self.bg.window_bottom
        return cx1-16, cy+5, cx2-16, cy+15