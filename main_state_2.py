from pico2d import *

import random
import json
import os

import game_framework
import game_world
import game_over_state
import pause_state
import main_state

from Boy import Boy
from hp_bar import HP_BAR

from ground_2 import Ground
from flatform import Flatform
#from back_ground import Background
from back_ground_2 import FixedBackground as Background
from spike import Spike
from monster_bear import Monster_bear
from monster_mage import Monster_mage
from chest import Chest
from heat_box import Heat_box
from gui import Gui
from flatform import Flatform
from flag import Flag

name = "MainState2"

boy = None
oldBoy = None
ground = []
FlatForm = None
background = None
Hp_Bar = None
Monster_Bear_List = []
Monster_Mage_List = []
ChestList = []
spikeList = []
font = None
GUI = None
FlatFormList = []
FLAG = None

def get_boy():
    return boy

def enter():
    global boy, oldBoy, background, ground

    background = Background()
    boy = Boy(background)
    oldBoy = main_state.get_boy()
    ground = [Ground(i, background) for i in range(len(Ground.groundList))]

    game_world.add_object(background, 0)
    for i in range(len(ground)):
        game_world.add_object(ground[i], 0)
    game_world.add_object(boy, 1)

    background.set_center_object(boy)
    boy.set_background(background)

    boy.x = 64*6
    boy.y = 64*4
    boy.itemList = oldBoy.itemList
    boy.magicList = oldBoy.magicList
    boy.fireSpellCount = oldBoy.fireSpellCount

def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
            boy.act_dash()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            boy.drinkPotion()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.spellLight()
        else:
            boy.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_s:
            boy.spellOnFire()
        elif event.type == SDL_KEYUP and event.key == SDLK_s:
            boy.spellOffFire()

        if event.type == SDL_KEYDOWN and event.key == SDLK_2:
            boy.openCure()
        elif event.type == SDL_KEYUP and event.key == SDLK_2:
            boy.closeCure()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def collide_flatform(a, b):
    left_a, bottom_a, right_a, top_a = a.get_flatform_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def update():
    global background
    for game_object in game_world.all_objects():
        game_object.update()

    print(background.window_left)
    print(background.canvas_width)
    print(background.w)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    draw_rectangle(100, 100, 800, 800)
    update_canvas()