import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

from sense_hat import SenseHat

sense = SenseHat(use_led_matrix=False)  # ← これが効く！

temp = sense.get_temperature()
print(f"Temperature: {temp:.2f}°C")
