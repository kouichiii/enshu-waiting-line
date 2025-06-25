import RPi.GPIO as GPIO
import cv2
import time
import datetime

# 超音波センサーのピン設定
TRIG = 15
ECHO = 14
SOUND_SPEED = 34300  # cm/s

# 撮影のしきい値（この距離以上なら撮影）
THRESHOLD_CM = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return -1
    start = time.time()

    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return -1
    end = time.time()

    distance = (end - start) * SOUND_SPEED / 2
    return distance

try:
    while True:
        dist = get_distance()
        if dist == -1:
            print("測距エラー")
        else:
            print(f"距離: {dist:.1f} cm")
            if dist >= THRESHOLD_CM:
                print("距離が離れたので撮影します")
                
                # 撮影処理
                dt_now = datetime.datetime.now()
                file_name = dt_now.strftime('%Y年%m月%d日%H時%M分%S秒') + '.jpg'
                
                cap = cv2.VideoCapture(0)
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(file_name, frame)
                    print(f"保存しました：{file_name}")
                cap.release()
                
                time.sleep(10)  # 撮影後に一定時間待機（多重撮影防止）
            else:
                print("近くに物体あり → 撮影しない")
        time.sleep(1)  # 次のチェックまで1秒待つ

except KeyboardInterrupt:
    print("終了します")
    GPIO.cleanup()
