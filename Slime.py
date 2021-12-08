from pico2d import *
import game_framework
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


MAP_WIDTH, MAP_HEIGHT = 1270, 717

PIXEL_PER_METER = (10.0 / 0.2) # 10 pixel 20 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

class slime():
    images = None
    font = None

    def __init__(self):
        self.image = load_image('Monster/slime/slime.png')
        self.frame = 0
        self.direction = 0

        if slime.font is None:
            slime.font = load_font('ENCR10B.TTF', 16)

        self.speed = 0
        self.timer = 1.0
        self.frame = 0
        self.build_behavior_tree()
        self.dir = random.random() * 2 * math.pi

        self.sizex, self.sizey = 50 ,50
        self.x, self.y = random.randint(150, 1130), random.randint(100, 635)

        self.t = 0
        self.hp = 100

    def wander(self):
        self.speed = RUN_SPEED_PPS

        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.random() * 2 * math.pi
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)

        self.bt = BehaviorTree(wander_node)

    def get_bb(self):
        return self.x - (self.sizex // 2), self.y - (self.sizey // 2), self.x + (self.sizex // 2), self.y + (self.sizey // 2)

    def draw(self):
        self.image.clip_draw(int(self.frame)*50, self.direction*50, 50, 50, self.x, self.y)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 30, self.y + 65, 'HP: %d' % self.hp, (255, 255, 0))

    def hited(self,knockback, damage):
        self.hp -= damage
        if self.direction == 3:
            self.x -= knockback
        elif self.direction == 2:
            self.x += knockback
        elif self.direction == 0:
            self.y -= knockback
        elif self.direction == 1:
            self.y += knockback

    def update(self):
        self.bt.run()
        self.frame = (self.frame +
                      FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(150, self.x, 1130)
        self.y = clamp(100, self.y, 635)

