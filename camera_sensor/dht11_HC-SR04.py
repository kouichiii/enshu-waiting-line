import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT

# --- GPIOピンの設定 ---
TRIG = 15
ECHO = 14
DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT11
speed_of_sound = 34370

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# --- 距離測定関数 ---
def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    timeout = time.time() + 1
    while not GPIO.input(ECHO):
        if time.time() > timeout:
            return -1
    t1 = time.time()

    while GPIO.input(ECHO):
        if time.time() > timeout:
            return -1
    t2 = time.time()

    return (t2 - t1) * speed_of_sound / 2

# --- メインループ ---
try:
    while True:
        # 距離
        distance = get_distance()
        if distance == -1:
            print("距離測定タイムアウト")
        else:
            print(f"\nDistance: {distance:.1f} cm")

        # 温湿度
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f} °C")
            print(f"Humidity: {humidity:.1f} %")
        else:
            print("DHT11 読み取りエラー")

        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("終了しました")
    sys.exit()
