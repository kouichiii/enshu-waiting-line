# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"  # ここでFB使用を回避！

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.show_letter("Z")
