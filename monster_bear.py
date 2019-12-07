from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_ATTACK_ACTION = 5

class Monster_bear:
    DamagedImage = None

    def __init__(self):
        self.x, self.y = 64*13, 64*2 + 64               # 64 = bear 높이 // 2
        self.HP = 150
        self.frame = 0
        self.image = load_image('image\Bear\Idle.png')
        self.HpBarImage = load_image('image\HP_Bar.png')
        if Monster_bear.DamagedImage == None:
            Monster_bear.DamagedImage = load_image('image\Damaged_HP_Bar_part.png')
        self.draw_per_damaged = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.HP <= 0:
            game_world.remove_object(self)
            self.y -= 1000

        self.draw_per_damaged = int(100 * (1.5 - self.HP * 0.01))

    def draw(self):
        self.image.clip_draw(40*int(self.frame), 0, 40, 40, self.x, self.y, 128, 128)
        draw_rectangle(*self.get_bb())
        self.HpBarImage.draw(50 + 123+300, 650)
        for i in range(self.draw_per_damaged):
            self.DamagedImage.draw(300 - 250+300 * (i * 0.01), 650)

    def get_bb(self):
        return self.x - 32, self.y - 60, self.x + 64, self.y + 50

    def damaged(self, damage):
        self.HP -= damage
        print(self.HP)