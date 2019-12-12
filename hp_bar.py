from pico2d import *
import game_framework
import game_over_state
import pause_state


class HP_BAR:
    damaged_image = None

    def __init__(self):
        self.image = load_image('image\HP_Bar.png')
        if HP_BAR.damaged_image == None:
            HP_BAR.damaged_image = load_image('image\Damaged_HP_Bar_part.png')
        self.draw_per_damaged = 0

    def draw(self):
        self.image.draw(50 + 123, 650)                  # 50+123, 550
        for i in range(self.draw_per_damaged):
            self.damaged_image.draw(300 - 250 * (i * 0.01), 650)

    def update(self):
        pass

    def trueUpdate(self, HP):
        self.draw_per_damaged = int(100 * (1 - HP * 0.01))