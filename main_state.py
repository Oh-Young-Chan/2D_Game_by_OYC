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

name = "MainState"

boy = None
ground = None
FlatForm = None
background = None
Hp_Bar = None
Monster_Bear = None
Monster_Mage = None
CHest = None
spike = None
font = None


def get_boy():
    return boy

def get_ground():
    return ground

def get_chest():
    return CHest

def get_Monster_Bear():
    return Monster_Bear

def get_Monster_Mage():
    return Monster_Mage


def enter():
    global boy, ground, FlatForm, background, spike, Hp_Bar, Monster_Bear, Monster_Mage, CHest, CHicken

    boy = Boy()
    Hp_Bar = HP_BAR()
    ground = Ground()
    FlatForm = Flatform()
    background = Background()
    Monster_Bear = Monster_bear()
    Monster_Mage = Monster_mage()
    spike = Spike()
    CHest = Chest()

    game_world.add_object(background, 0)
    game_world.add_object(ground, 0)
    game_world.add_object(FlatForm, 1)
    game_world.add_object(boy, 2)
    game_world.add_object(Monster_Bear, 1)
    game_world.add_object(Monster_Mage, 1)
    game_world.add_object(spike, 1)
    game_world.add_object(CHest, 1)

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            boy.act_attack()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
            boy.act_dash()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            boy.eatChicken()
        else:
            boy.handle_event(event)

        if event.type == SDL_KEYDOWN and event.key == SDLK_w:
            boy.openCure()
        elif event.type == SDL_KEYUP and event.key == SDLK_w:
            boy.closeCure()

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

    if collide(boy, Monster_Mage):
        boy.damaged(1)
    if collide(boy, Monster_Bear):
        boy.damaged(3)
    if collide(boy, spike):
        boy.damaged(5)

    if collide_flatform(boy, FlatForm):
        boy.stop()

    Hp_Bar.update(boy.HP)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    Hp_Bar.draw()
    update_canvas()

