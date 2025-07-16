#!/usr/bin/env python3
"""
Node A (HC-SR04 + USB/CSI カメラ)
  1. 超音波センサーで距離測定
  2. しきい値(30 cm)を超えたら cv2 で撮影
  3. Node B (Sense HAT) へ HTTP GET し温度・湿度取得
  4. 撮影ファイル名と温湿度を表示
"""
import time, datetime, statistics, requests, signal, sys
from pathlib import Path

import RPi.GPIO as GPIO
import cv2

# ── ハード設定 ───────────────────────────────────────
TRIG, ECHO   = 15, 14
THRESHOLD_CM = 30
MEASURE_NUM  = 3                   # 距離を何回取って中央値か
SOUND_SPEED  = 34300               # cm/s

# ── パス設定 ─────────────────────────────────────────
CAP_DIR = Path.home() / "capture"
CAP_DIR.mkdir(parents=True, exist_ok=True)

# ── Node B エンドポイント ────────────────────────────
NODE_B_URL = "http://172.16.1.27:5000/sensor"   # ★自分の IP に合わせる

# ── GPIO 初期化 ─────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

# ── カメラ（OpenCV）初期化 ───────────────────────────
# 毎回 open/close でも動きますが、ここで 1 度だけ開いて再利用すると高速
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

def cleanup(sig=None, frm=None):
    print("終了処理 …")
    cap.release()
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,  cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ── 距離測定関数 ─────────────────────────────────────
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

# ── 撮影関数 (OpenCV) ─────────────────────────────────
def capture_image() -> Path:
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CAP_DIR / f"img_{ts}.jpg"

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(str(path), frame)
    else:
        print("⚠ 画像取得失敗")
    return path

# ── 温湿度取得 ───────────────────────────────────────
def fetch_temp_humi():
    try:
        r = requests.get(NODE_B_URL, timeout=2)
        r.raise_for_status()
        js = r.json()
        return js.get("temperature"), js.get("humidity")
    except Exception as e:
        print("温湿度取得失敗:", e)
        return None, None

# ── メインループ ────────────────────────────────────
print("Node A (cv2 版) 起動。距離を測定しています …")
while True:
    dist = get_distance()
    print(f"距離: {dist:.1f} cm")
    if dist >= THRESHOLD_CM:
        print(" └ しきい値超過 → 撮影")
        img_path = capture_image()

        temp, humi = fetch_temp_humi()
        print(f"   撮影: {img_path.name}")
        print(f"   温度={temp} ℃, 湿度={humi} %")

        time.sleep(10)          # 多重撮影防止
    time.sleep(1)
