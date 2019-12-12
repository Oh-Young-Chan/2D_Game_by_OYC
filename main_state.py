from pico2d import *

import random
import json
import os

import game_framework
import game_world
import game_over_state
import pause_state
import main_state_2
import clear_game_state

from Boy import Boy
from hp_bar import HP_BAR
from ground import Ground
from flatform import Flatform
#from back_ground import Background
from back_ground import FixedBackground as Background
from spike import Spike
from monster_bear import Monster_bear
from monster_mage import Monster_mage
from chest import Chest
from heat_box import Heat_box
from gui import Gui
from flatform import Flatform
from flag import Flag

name = "MainState"

boy = None
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

def get_ground():
    return ground

def get_flatform():
    return FlatFormList

def get_Bground():
    return background

def get_Monster_Bear_List():
    return Monster_Bear_List

def get_Monster_Mage_List():
    return Monster_Mage_List


def enter():
    global boy, ground, background, spikeList, Hp_Bar, Monster_Bear_List, Monster_Mage_List, ChestList, CHicken,\
        GUI, FlatFormList, FLAG

    background = Background()
    boy = Boy(background)
    Hp_Bar = HP_BAR()
    ground = [Ground(i, background) for i in range(len(Ground.groundList))]
    Monster_Bear_List = [Monster_bear(i, background) for i in range(len(Monster_bear.posList))]
    Monster_Mage_List = [Monster_mage(i) for i in range(len(Monster_mage.posList))]
    spikeList = [Spike(i, background) for i in range(len(Spike.spikeList))]
    ChestList = [Chest(i, background) for i in range(len(Chest.chestList))]
    GUI = Gui()
    FlatFormList = [Flatform(i, background) for i in range(len(Flatform.flatFormList))]
    FLAG = Flag(background)

    game_world.add_object(background, 0)
    for i in range(len(ground)):
        game_world.add_object(ground[i], 0)
    game_world.add_object(boy, 2)
    game_world.add_object(Hp_Bar, 1)
    for i in range(len(Monster_Bear_List)):
        game_world.add_object(Monster_Bear_List[i], 1)
    for i in range(len(Monster_Mage_List)):
        game_world.add_object(Monster_Mage_List[i], 1)
    for i in range(len(ChestList)):
        game_world.add_object(ChestList[i], 1)
    for i in range(len(spikeList)):
        game_world.add_object(spikeList[i], 1)
    game_world.add_object(GUI, 1)
    for i in range(len(FlatFormList)):
        game_world.add_object((FlatFormList[i]), 1)
    game_world.add_object(FLAG, 1)

    background.set_center_object(boy)
    boy.set_background(background)

def get_ground():
    return ground

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x:
            boy.onJump()
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

        for i in range(len(ChestList)):
            if collide(boy, ChestList[i]):
                if event.type == SDL_KEYDOWN and event.key == SDLK_UP:
                    ChestList[i].open()
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
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[1]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[2]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[3]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[4]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[5]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[6]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[7]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[8]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[9]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[10]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[11]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[12]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[13]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[14]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[15]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[16]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[17]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[18]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[19]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[20]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[21]):
        boy.flatform_stop()
        boy.workingJump = True
    elif collide_flatform(boy, FlatFormList[22]):
        boy.flatform_stop()
        boy.workingJump = True

    else:
        boy.onFlatform = False

    for i in range(len(spikeList)):
        if collide(boy, spikeList[i]):
            boy.damaged(5)

    Monster_Bear_List[0].x = clamp(0, Monster_Bear_List[0].x, 1000)
    Monster_Bear_List[1].x = clamp(0, Monster_Bear_List[1].x, 1000)
    Monster_Bear_List[2].x = clamp(0, Monster_Bear_List[2].x, 1000)
    Monster_Bear_List[3].x = clamp(1050, Monster_Bear_List[3].x, 1950)
    Monster_Bear_List[4].x = clamp(1050, Monster_Bear_List[4].x, 1950)

    if collide(boy, FLAG):
        game_framework.change_state(clear_game_state)

    Hp_Bar.trueUpdate(boy.HP)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

