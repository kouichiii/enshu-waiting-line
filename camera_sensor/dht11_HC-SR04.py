import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO4（物理ピン7）

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print(f"温度: {temperature:.1f} °C")
    print(f"湿度: {humidity:.1f} %")
else:
    print("DHT11 読み取りエラー：配線またはセンサの問題です")
