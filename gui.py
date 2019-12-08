from pico2d import *
import game_framework
import main_state


class Gui:
    def __init__(self):
        self.moneyX, self.moneyY = 80, 600
        self.potionX, self.potionY = 180, 600

        self.lightningBookX, self.lightningBookY = 80, 550
        self.fireBookX, self.fireBookY = 160, 550
        self.healBookX, self.healBookY = 240, 550

        self.strX, self.strY = 60, 500
        self.intX, self.intY = 60, 480

        self.moneyImage = load_image('image\Money_Pack.png')
        self.potionImage = load_image('image\Item\Red_Potion.png')

        self.lightningBookImage = load_image('image\Item\Lightning_Book.png')
        self.fireBookImage = load_image('image\Item\Fire_Book.png')
        self.healBookImage = load_image('image\Item\Heal_Book.png')

        self.font = load_font('ConsolaMalgun.ttf', 32)
        self.fontStatus = load_font('ConsolaMalgun.ttf', 16)

        self.boy = main_state.get_boy()

        self.moneyCount = 0
        self.potionCount = 0

        self.lightningBookCount = 0
        self.fireBookCount = 0
        self.healBookCount = 0

        self.STR = self.boy.STR
        self.INT = self.boy.INT


    def draw(self):
        self.moneyImage.draw(self.moneyX, self.moneyY)
        self.font.draw(self.moneyX+20, self.moneyY, '%d' % self.moneyCount, (0, 0, 0))
        self.potionImage.draw(self.potionX, self.potionY)
        self.font.draw(self.potionX+20, self.potionY, '%d' % self.potionCount, (0, 0, 0))

        self.lightningBookImage.draw(self.lightningBookX, self.lightningBookY)
        self.font.draw(self.lightningBookX+30, self.lightningBookY, '%d' % self.lightningBookCount, (0, 0, 0))
        self.fireBookImage.draw(self.fireBookX, self.fireBookY)
        self.font.draw(self.fireBookX + 30, self.fireBookY, '%d' % self.fireBookCount, (0, 0, 0))
        self.healBookImage.draw(self.healBookX, self.healBookY)
        self.font.draw(self.healBookX + 30, self.healBookY, '%d' % self.healBookCount, (0, 0, 0))

        self.fontStatus.draw(self.strX, self.strY, 'STR : %d' % self.STR, (0, 0, 0))
        self.fontStatus.draw(self.intX, self.intY, 'INT : %d' % self.INT, (0, 0, 0))


    def update(self):
        self.moneyCount = self.boy.coinCount
        self.potionCount = len(self.boy.itemList[0])

        self.lightningBookCount = len(self.boy.magicList[0])
        self.fireBookCount = self.boy.fireSpellCount
        self.healBookCount = len(self.boy.magicList[2])

        self.STR = self.boy.STR
        self.INT = self.boy.INT