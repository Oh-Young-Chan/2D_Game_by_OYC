from pico2d import *
import game_framework
import game_world
import random

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Monster_mage:
    DamagedImage = None
    posList = []

    def __init__(self, i):
        self.x, self.y = self.posList[i], 64*2+45                          # 45 = Mage높이 // 2
        self.HP = 80
        self.frame = random.randrange(0, 9)
        self.deathFrame = 0
        self.removing = False
        self.image = load_image('image\Mage\Attack.png')
        self.deathImage = load_image('image\Mage\Death.png')
        self.HpBarImage = load_image('image\HP_Bar.png')
        if Monster_mage.DamagedImage == None:
            Monster_mage.DamagedImage = load_image('image\Damaged_HP_Bar_part.png')
        self.draw_per_damaged = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.draw_per_damaged = int(100 * ((0.8 - self.HP * 0.01) / 0.8))                           # int(100* ((HP통 - self.HP*0.01) / HP통)
        if self.HP <= 0:
            self.deathFrame = (self.deathFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (6+1)
            if self.deathFrame >= 6:
                game_world.remove_object(self)
                self.y -= 1000

    def draw(self):
        if self.removing:
            pass
        else:
            self.image.clip_composite_draw(32*int(self.frame), 0, 32, 32, 0, 'h', self.x, self.y, 89, 89)
        draw_rectangle(*self.get_bb())
        self.drawHpBar()
        if self.HP <= 0:
            self.drawDeath()
            self.removing = True

    def drawHpBar(self):
        self.HpBarImage.draw(self.x - 15, self.y - 60, 100, 8)
        for i in range(self.draw_per_damaged):
            self.DamagedImage.draw(self.x - 15 + (100 // 2) - 100 * (i * 0.01), self.y - 60, 1,
                                   8)  # (self.x+위치조정+HP바draw크기//2)-HP바draw크기*(i*0.01), self.y-위치조정

    def drawDeath(self):
        self.deathImage.clip_composite_draw(32*int(self.deathFrame), 0, 32, 32, 0, 'h', self.x, self.y, 89, 89)

    def get_bb(self):
        return self.x - 55, self.y - 40, self.x + 35, self.y + 40

    def damaged(self, damage, fire):
        self.HP -= damage
        if fire:
            pass