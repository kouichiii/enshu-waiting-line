from sense_hat import SenseHat
import time

sense = SenseHat()

# 背景色（黒）と文字色（赤）
sense.show_message("Hello!", text_colour=[255, 0, 0], back_colour=[0, 0, 0])
