#!/usr/bin/env python3
from sense_hat import SenseHat
import time

sense = SenseHat()

def read_temperature():
    temp_h = sense.get_temperature_from_humidity()
    temp_p = sense.get_temperature_from_pressure()
    temp = (temp_h + temp_p) / 2  # 平均をとるとより安定
    return round(temp, 2)

try:
    while True:
        temp = read_temperature()
        print(f"Current Temperature: {temp} °C")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
