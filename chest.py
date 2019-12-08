from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

from potion import Potion
from coin import Coin
from lightning_book import Lightning_Book
from fire_book import Fire_Book

class Chest:
    def __init__(self):
        self.x, self.y = 64*15, 64*2 + 32                       # 32 = chest의 높이 // 2
        self.image = load_image('image\Golden_Chest.png')
        self.frame = 0
        self.openning = False
        self.openCount = 1
        #self.itemList = [Potion(self.x, self.y), Potion(self.x, self.y+320), Fire_Book(self.x, self.y),
         #                Coin(self.x+30, self.y+30), Lightning_Book(self.x, self.y)]
        self.itemList = [Potion(self.x, self.y), Fire_Book(self.x, self.y), Lightning_Book(self.x, self.y),
                         Coin(self.x, self.y),Coin(self.x, self.y),Coin(self.x, self.y),Coin(self.x, self.y),]

    def update(self):
        if self.openning:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%8
            if self.frame>=7:
                self.frame = 7



    def draw(self):
        self.image.clip_draw(32*int(self.frame), 0, 32, 32, self.x, self.y, 64, 64)
        draw_rectangle(*self.get_bb())

    def createItem(self):
        for i in self.itemList:
            game_world.add_object(i, 2)


    def open(self):
        #print('open')
        self.openCount -= 1
        if self.openCount == 0:
            self.openning = True
            self.createItem()

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 16, self.y