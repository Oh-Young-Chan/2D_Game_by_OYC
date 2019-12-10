from pico2d import *

import random
import json
import os

import game_framework
import game_world
import game_over_state
import pause_state

from Boy import Boy
from hp_bar import HP_BAR
from ground import Ground
from flatform import Flatform
from back_ground import Background
from spike import Spike
from monster_bear import Monster_bear
from monster_mage import Monster_mage
from chest import Chest
from heat_box import Heat_box
from gui import Gui
from flatform import Flatform
from ladder import Ladder

name = "MainState"

boy = None
ground = None
FlatForm = None
background = None
Hp_Bar = None
Monster_Bear_List = []
Monster_Mage_List = []
CHest = None
spike = None
font = None
GUI = None
FlatFormList = []
LaDder = None


def get_boy():
    return boy

def get_ground():
    return ground

def get_chest():
    return CHest

def get_Monster_Bear_List():
    return Monster_Bear_List

def get_Monster_Mage_List():
    return Monster_Mage_List


def enter():
    global boy, ground, background, spike, Hp_Bar, Monster_Bear_List, Monster_Mage_List, CHest, CHicken,\
        GUI, FlatFormList, LaDder

    boy = Boy()
    Hp_Bar = HP_BAR()
    ground = Ground()
    background = Background()
    Monster_Bear_List = [Monster_bear(i) for i in range(5)]
    Monster_Mage_List = [Monster_mage(i) for i in range(3)]
    spike = Spike()
    CHest = Chest()
    GUI = Gui()
    FlatFormList = [Flatform(i) for i in range(len(Flatform.flatFormList))]
    LaDder = Ladder(300, 64*2+16)

    game_world.add_object(background, 0)
    game_world.add_object(ground, 0)
    game_world.add_object(boy, 2)
    for i in range(len(Monster_Bear_List)):
        game_world.add_object(Monster_Bear_List[i], 1)
    for i in range(len(Monster_Mage_List)):
        game_world.add_object(Monster_Mage_List[i], 1)
    game_world.add_object(spike, 1)
    game_world.add_object(CHest, 1)
    game_world.add_object(GUI, 1)
    for i in range(len(FlatFormList)):
        game_world.add_object((FlatFormList[i]), 1)
    game_world.add_object(LaDder, 1)

def get_ground():
    return ground

def exit():
    global Hp_Bar

    game_world.clear()
    del Hp_Bar


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

        if collide(boy, LaDder):
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                boy.climb_ladder()
        else:
            boy.onLadder = False

        if collide(boy, CHest):
            if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                CHest.open()
    if boy.HP <= 0:
        game_framework.change_state(game_over_state)


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
    for game_object in game_world.all_objects():
        game_object.update()

    for i in range(len(Monster_Mage_List)):
        if collide(boy, Monster_Mage_List[i]):
            boy.damaged(1)
    for i in range(len(Monster_Bear_List)):
        if collide(boy, Monster_Bear_List[i]):
            boy.damaged(3)

# --------------------플랫폼 충돌---------------------------
    if collide_flatform(boy, FlatFormList[0]):
        boy.flatform_stop()
    elif collide_flatform(boy, FlatFormList[1]):
        boy.flatform_stop()
    elif collide_flatform(boy, FlatFormList[2]):
        boy.flatform_stop()
    elif collide_flatform(boy, FlatFormList[3]):
        boy.flatform_stop()
    elif collide_flatform(boy, FlatFormList[4]):
        boy.flatform_stop()
    elif collide_flatform(boy, FlatFormList[5]):
        boy.flatform_stop()
    else:
        boy.onFlatform = False

    if collide(boy, spike):
        boy.damaged(5)

    Hp_Bar.update(boy.HP)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    Hp_Bar.draw()
    update_canvas()

