from pico2d import *
import game_framework
import game_world
import main_state

class Ladder:
    ladderDown = None
    ladderMiddle = None
    ladderTop = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if Ladder.ladderDown == None:
            Ladder.ladderDown = load_image('image\Ladder_down.png')
        if Ladder.ladderMiddle == None:
            Ladder.ladderMiddle = load_image('image\Ladder_middle.png')
        if Ladder.ladderTop == None:
            Ladder.ladderTop = load_image('image\Ladder_top.png')

    def draw(self):
        self.ladderDown.draw(self.x, self.y)
        self.ladderMiddle.draw(self.x, self.y+32)
        self.ladderTop.draw(self.x, self.y+32*2)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x-8, self.y-16, self.x+8, self.y+80