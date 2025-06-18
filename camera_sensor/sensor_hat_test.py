import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # PygameにFBを使わせない（最重要）

from sense_hat import SenseHat
import time

sense = SenseHat()

# 全消灯しておく
sense.clear()

# 青色で "Hello" を表示
sense.show_message("Hello!", text_colour=[0, 0, 255], back_colour=[0, 0, 0])

# 消灯
sense.clear()
