from pico2d import *
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import game_world
import main_state
import random

from coin import Coin
from potion import Potion
from lightning_book import Lightning_Book
from fire_book import Fire_Book

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4
FRAMES_PER_DEATH_ACTION = 6


class Monster_bear:
    DamagedImage = None
    posList = [(500, 550), (500, 360+64*14), (600, 360+64*14), (1400, 360+64*10-32), (1700, 360+64*10-32)]

    def __init__(self, i, bg):
        self.bg = bg
        self.x, self.y = self.posList[i]  # 64*13, 64 = bear 높이 // 2
        self.HP = 150
        self.frame = random.randrange(0, 5)
        self.hurtFrame = 0
        self.deathFrame = 0
        self.hurting = False
        self.removing = False
        self.font = load_font('ConsolaMalgun.ttf', 16)
        self.writeDamage = 0
        self.hitCount = 0
        self.dropItemCount = random.randrange(4)
        self.dropItemSort = random.randrange(1, 10+1)
        self.image = load_image('image\Bear\Idle.png')
        self.hurtImage = load_image('image\Bear\Hurt.png')
        self.deathImage = load_image('image/Bear/Death.png')
        self.HpBarImage = load_image('image\HP_Bar.png')
        if Monster_bear.DamagedImage == None:
            Monster_bear.DamagedImage = load_image('image\Damaged_HP_Bar_part.png')
        self.dir = 1
        self.speed = 0
        self.timer = 1.0
        self.build_behavior_tree()
        self.draw_per_damaged = 0
        self.boy = main_state.get_boy()

    def calculate_current_position(self):
        self.x += self.speed * self.dir * game_framework.frame_time

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.randrange(-1, 2)

    def find_player(self):
        boy = main_state.get_boy()
        distance = (boy.x - self.x) ** 2 + (boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 1500):
            if boy.x - self.x < 0:
                self.dir = -1
            elif boy.x - self.x >= 0:
                self.dir = 1
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return  BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wander_node = LeafNode('Wander', self.wander)
        find_player_node = LeafNode('Find Player', self.find_player)
        move_to_player_node = LeafNode('Move to Player', self.move_to_player)
        chase_node = SequenceNode('Chase')
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode('WanderChase')
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.draw_per_damaged = int(100 * ((1.5 - self.HP * 0.01) / 1.5))  # int(100* ((HP통
        # - self.HP*0.01) / HP통)
        if self.hurting:
            self.hurtFrame = (self.hurtFrame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        else:
            self.hurtFrame = 0
        if self.HP <= 0:
            self.deathFrame = (self.deathFrame + FRAMES_PER_DEATH_ACTION * ACTION_PER_TIME * game_framework.frame_time) % (6+1)
            if self.deathFrame >= 6:
                self.drop_item()
                game_world.remove_object(self)
                self.y -= 1000

        self.HP = clamp(0, self.HP, 150)
        self.bt.run()


    def draw(self):
        cx, cy = self.x - self.bg.window_left, self.y-self.bg.window_bottom
        if self.removing:  # HP가 0보다 낮아져 죽으면
            self.drawDeath()  # 죽음 애니메이션
        else:  # 아니면
            if self.hurting:  # 맞았을 때
                self.hurtImage.clip_draw(40 * int(self.hurtFrame), 0, 40, 40, cx, cy, 128, 128)  # 맞는 모션 애니메이션
                if self.hurtFrame >= 3:  # 애니메이션 프레임 한 바퀴 돌면
                    self.hurting = False  # 맞는 모션 애니메이션 중단
                    self.hitCount = 0  # 맞고 실행할 거 다 했으니 다시 맞은 개수 초기화
            else:  # 죽지도 맞지도 않는 경우(평상시)
                self.image.clip_draw(40 * int(self.frame), 0, 40, 40, cx, cy, 128, 128)  # Idle 애니메이션
        self.drawHpBar()
        if self.HP <= 0:
            self.removing = True
        if self.writeDamage == 0:
            pass
        else:
            if self.hurting:
                self.font.draw(cx, cy + 64, '-%d' % self.writeDamage, (255, 0, 0))

    def drawHpBar(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.HpBarImage.draw(cx + 15, cy - 80, 100, 8)
        for i in range(self.draw_per_damaged):
            self.DamagedImage.draw(cx + 15 + (100 // 2) - 100 * (i * 0.01), cy - 80, 1,
                                   8)  # (self.x+HP바draw크기//2)-HP바draw크기*(i*0.01)

    def drawDeath(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.deathImage.clip_draw(40 * int(self.deathFrame), 0, 40, 40, cx, cy, 128, 128)

    def get_bb(self):
        cx, cy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        return cx - 32, cy - 60, cx + 64, cy + 50

    def damaged(self, damage, fire):
        self.writeDamage = damage
        # if 3 <= self.boy.attackFrame < 3.2:
        if fire:
            pass
        else:
            if self.dir == 1:
                self.x -= 500 * game_framework.frame_time
            else:
                self.x += 500 * game_framework.frame_time
        if self.hitCount == 0:  # 한 번 맞으면 대미지 안입음
            self.HP -= damage
            self.hitCount = 1  # 한 번 맞았으니 올려줌
        else:
            pass
        self.hurt()

    def hurt(self):
        self.hurting = True

    def drop_item(self):
        for i in range(self.dropItemCount):
            if 1 <= self.dropItemSort+i <= 5:
                game_world.add_object(Coin(self.x, self.y, self.bg), 2) # update()에서 현재 좌표 해서 해결
            elif 6 <= self.dropItemSort+i <= 8:
                game_world.add_object(Potion(self.x, self.y, self.bg), 2)
            elif self.dropItemSort+i == 9:
                game_world.add_object(Lightning_Book(self.x, self.y, self.bg), 2)
            else:
                game_world.add_object(Fire_Book(self.x, self.y, self.bg), 2)