import game_framework
from pico2d import *

import start_state

open_canvas(1280, 720, sync=True)
game_framework.run(start_state)
close_canvas()