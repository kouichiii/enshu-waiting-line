from sense_hat import SenseHat
import time

sense = SenseHat()

while True:
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    print(f"🌡 温度: {temp:.1f} °C")
    print(f"💧 湿度: {humidity:.1f} %")
    print(f"📈 気圧: {pressure:.1f} hPa")
    print("-" * 30)

    time.sleep(2)
