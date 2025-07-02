#!/usr/bin/env python3
"""
Node A  (HC-SR04 + PiCamera2 搭載 Raspberry Pi)
  1. HC-SR04 で距離を測定
  2. 30 cm 以上なら写真撮影
  3. Node B へ HTTP GET し温度・湿度を取得
  4. 取得結果をコンソールに表示（送信はここでは行わない）
"""

import os, time, datetime, statistics, signal, sys, requests
import RPi.GPIO as GPIO
from picamera2 import Picamera2

# ── 設定 ───────────────────────────────────────────────────
TRIG, ECHO   = 15, 14         # HC-SR04 ピン
THRESHOLD_CM = 30             # 撮影トリガ距離
MEASURE_NUM  = 3              # 測距回数（中央値）
CAP_DIR      = "/home/pi/capture"
os.makedirs(CAP_DIR, exist_ok=True)

NODE_B_URL   = "http://172.16.1.96:5000/sensor"   # ★ Node B の IP に書き換え172.16.1.96

# ── GPIO & カメラ初期化 ───────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
SOUND_SPEED  = 34300  # cm/s

camera = Picamera2()
camera.configure(camera.create_still_configuration({"size": (1920, 1080)}))
camera.start()

def cleanup(sig=None, frm=None):
    print("終了処理…")
    camera.close()
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,  cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ── 距離計測 ───────────────────────────────────────────────
def one_distance():
    GPIO.output(TRIG, 1)
    time.sleep(1e-5)
    GPIO.output(TRIG, 0)

    t0 = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - t0 < 0.02:
        pass
    t1 = time.time()

    while GPIO.input(ECHO) == 1 and time.time() - t1 < 0.02:
        pass
    return (time.time() - t1) * SOUND_SPEED / 2

def get_distance():
    return statistics.median(one_distance() for _ in range(MEASURE_NUM))

# ── カメラ撮影 ────────────────────────────────────────────
def capture_image() -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(CAP_DIR, f"img_{ts}.jpg")
    camera.capture_file(path)
    return path

# ── Node B から温湿度取得 ─────────────────────────────────
def fetch_temp_humi():
    try:
        r = requests.get(NODE_B_URL, timeout=2)
        r.raise_for_status()
        j = r.json()
        return j["temperature"], j["humidity"]
    except Exception as e:
        print("温湿度取得失敗:", e)
        return None, None

# ── メインループ ─────────────────────────────────────────
print("Node A 起動。距離を測定中…")
while True:
    dist = get_distance()
    print(f"距離: {dist:.1f} cm")
    if dist >= THRESHOLD_CM:
        print(" └ しきい値超過！撮影します")
        img_path = capture_image()
        temp, humi = fetch_temp_humi()
        print(f"   撮影完了: {os.path.basename(img_path)}")
        print(f"   温度={temp} ℃, 湿度={humi}%")
        time.sleep(10)  # 多重撮影防止
    time.sleep(1)
