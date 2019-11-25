import game_framework
from pico2d import *

import start_state

open_canvas(800, 600, sync=True)
game_framework.run(start_state)
close_canvas()