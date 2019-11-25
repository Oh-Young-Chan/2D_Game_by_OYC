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

name = "MainState"

boy = None
ground = None
background = None
Hp_Bar = None
Monster_Bear = None
Monster_Mage = None
spike = None
font = None

def enter():
    global boy, ground, background, spike, Hp_Bar, Monster_Bear, Monster_Mage

    boy = Boy()
    Hp_Bar = HP_BAR()
    ground = Ground()
    background = Background()
    Monster_Bear = Monster_bear()
    Monster_Mage = Monster_mage()
    spike = Spike()

    game_world.add_object(background, 0)
    game_world.add_object(ground, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(Monster_Bear, 1)
    game_world.add_object(Monster_Mage, 1)
    game_world.add_object(spike, 1)


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
        else:
            boy.handle_event(event)
    if boy.HP == 0:
        game_framework.change_state(game_over_state)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if boy.x >= 600:
        boy.damaged(10)

    Hp_Bar.update(boy.HP)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    Hp_Bar.draw()
    update_canvas()

