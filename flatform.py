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
    flatFormList = [(500, 550, 200), (500, 550, 300), (500, 550, 400), (550, 600, 400), (600, 650, 400), (400, 800, 500)]

    def __init__(self, i):
        self.x1, self.x2, self.y = self.flatFormList[i]
        if Flatform.startFlatForm == None:
            Flatform.startFlatForm = load_image('image\FlatForm_01.png')
        if Flatform.middleFlatForm == None:
            Flatform.middleFlatForm = load_image('image\FlatForm_02.png')
        if Flatform.endFlatForm == None:
            Flatform.endFlatForm = load_image('image\FlatForm_03.png')

    def draw(self):
        if (self.x2-self.x1) < 32:
            self.middleFlatForm.draw(self.x1, self.y)
        elif 32 < (self.x2-self.x1) < 64:
            self.middleFlatForm.draw(self.x1, self.y)
            self.middleFlatForm.draw(self.x2-32, self.y)
        elif 64 < (self.x2-self.x1) < 96:
            self.middleFlatForm.draw(self.x1, self.y)
            self.middleFlatForm.draw(self.x1+32, self.y)
            self.middleFlatForm.draw(self.x2-32, self.y)
        elif 96 < (self.x2-self.x1):
            self.startFlatForm.draw(self.x1, self.y)
            for i in range(1, (self.x2-self.x1-64)//32 + 1):
                self.middleFlatForm.draw(self.x1+32*i, self.y)
            self.middleFlatForm.draw(self.x1+32*((self.x2-self.x1-64)//32) + (self.x2-self.x1-64)%32, self.y)
            self.endFlatForm.draw(self.x2-32, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x1-16, self.y+5, self.x2-16, self.y+15