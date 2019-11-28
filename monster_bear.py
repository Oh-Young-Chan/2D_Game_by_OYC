from pico2d import *
import game_framework
import game_world

class Monster_bear:
    def __init__(self):
        self.x, self.y = 500, 120
        self.HP = 150
        self.frame = 0
        self.image = load_image('Bear.png')

    def update(self):
        self.frame = (self.frame+1) % 4

        if self.HP <= 0:
            game_world.remove_object(self)
            self.y -= 1000

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 60, self.y - 60, self.x + 60, self.y + 60

    def damaged(self, damage):
        self.HP -= damage
        print(self.HP)