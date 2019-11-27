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
from back_ground import Background
from spike import Spike
from monster_bear import Monster_bear
from monster_mage import Monster_mage
from health_item import Health_item

name = "MainState"

boy = None
ground = None
background = None
Hp_Bar = None
Monster_Bear = None
Monster_Mage = None
Health_Item = None
spike = None
font = None

def enter():
    global boy, ground, background, spike, Hp_Bar, Monster_Bear, Monster_Mage, Health_Item

    boy = Boy()
    Hp_Bar = HP_BAR()
    ground = Ground()
    background = Background()
    Monster_Bear = Monster_bear()
    Monster_Mage = Monster_mage()
    spike = Spike()
    Health_Item = Health_item()

    game_world.add_object(background, 0)
    game_world.add_object(ground, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(Monster_Bear, 1)
    game_world.add_object(Monster_Mage, 1)
    game_world.add_object(spike, 1)
    game_world.add_object(Health_Item, 1)


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
        else:
            boy.handle_event(event)
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

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if collide(boy, Monster_Mage):
        boy.damaged(0)
    if collide(boy, Monster_Bear):
        boy.damaged(0)
    if collide(boy, spike):
        boy.damaged(0)

    if collide(boy, Health_Item):
        boy.recovery(50)
        game_world.remove_object(Health_Item)
        Health_Item.y -= 100

    Hp_Bar.update(boy.HP)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    Hp_Bar.draw()
    update_canvas()

