import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # ここでFB使用を回避！

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()
sense.show_message("Hello!", text_colour=[255, 0, 0], back_colour=[0, 0, 0])
