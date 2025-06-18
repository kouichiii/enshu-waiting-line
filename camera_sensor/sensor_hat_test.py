from sense_hat import SenseHat
sense = SenseHat()

temp = sense.get_temperature()
humidity = sense.get_humidity()
pressure = sense.get_pressure()

print(f"温度: {temp:.2f} ℃")
print(f"湿度: {humidity:.2f} %")
print(f"気圧: {pressure:.2f} hPa")
