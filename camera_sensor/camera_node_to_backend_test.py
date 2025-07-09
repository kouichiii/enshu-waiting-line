#!/usr/bin/env python3
"""
Node A (HC-SR04 + OpenCV カメラ)
  1. 距離測定
  2. しきい値以上で撮影
  3. Node B へ GET → 温湿度取得
  4. Node C へ multipart/form-data で画像 + 温湿度を POST
"""
import time, datetime, statistics, signal, sys
from pathlib import Path
import requests                       # ←★ Node C 送信用
import RPi.GPIO as GPIO
import cv2

# ── 固定設定 ──────────────────────────────────────────
TRIG, ECHO   = 15, 14
THRESHOLD_CM = 30
MEASURE_NUM  = 3
SOUND_SPEED  = 34300                  # cm/s

CAP_DIR = Path("/home/y-hashimoto/Documents/test/enshu-waiting-line/camera/sensor/capture")
CAP_DIR.mkdir(parents=True, exist_ok=True)

NODE_B_URL = "http://172.16.1.27:5000/sensor"         # 温湿度 API
NODE_C_URL = "http://172.16.1.33:8000/api/upload"     # ★送信先
DEVICE_ID  = "2"                                      # 固定 ID

SEND_TEST = 1

# ── GPIO ────────────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

# ── カメラ ──────────────────────────────────────────
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

def cleanup(sig=None, frm=None):
    cap.release()
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT,  cleanup)
signal.signal(signal.SIGTERM, cleanup)

# ── 距離測定 ─────────────────────────────────────────
def one_distance():
    GPIO.output(TRIG, 1); time.sleep(1e-5); GPIO.output(TRIG, 0)
    t0 = time.time()
    while GPIO.input(ECHO) == 0 and time.time() - t0 < 0.02: pass
    t1 = time.time()
    while GPIO.input(ECHO) == 1 and time.time() - t1 < 0.02: pass
    return (time.time() - t1) * SOUND_SPEED / 2

def get_distance():
    return statistics.median(one_distance() for _ in range(MEASURE_NUM))

# ── 撮影 ────────────────────────────────────────────
def capture_image() -> Path:
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CAP_DIR / f"img_{ts}.jpg"
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(str(path), frame)
    else:
        print("⚠ 画像取得失敗")
    return path

# ── Node B から温湿度取得 ───────────────────────────
def fetch_temp_humi():
    try:
        r = requests.get(NODE_B_URL, timeout=2)
        r.raise_for_status()
        js = r.json()
        return js.get("temperature"), js.get("humidity")
    except Exception as e:
        print("温湿度取得失敗:", e)
        return None, None

# ── Node C へ送信 ──────────────────────────────────
def send_to_node_c(img_path: Path, temp, humi):
    try:
        with open(img_path, "rb") as f:
            files = {"image": f}
            data  = {
                "device_id":  DEVICE_ID,
                "temperature": f"{temp:.1f}" if temp is not None else "",
                "humidity":    f"{humi:.1f}" if humi is not None else ""
            }
            resp = requests.post(NODE_C_URL, files=files, data=data, timeout=5)
        print(f"Node C → {resp.status_code}: {resp.text[:80]}")
    except Exception as e:
        print("Node C 送信例外:", e)

# ── メインループ ───────────────────────────────────
print("Node A 起動 – 距離測定中 …")
while True:
    dist = get_distance()
    print(f"距離: {dist:.1f} cm")
    if dist >= THRESHOLD_CM:
        print(" └ しきい値超過 → 撮影")
        if SEND_TEST == 1:
            img = CAP_DIR / "sample2.jpg"
            print(f"★ テストモード: sample2.jpg を送信します → {img}")
        else:
            img = capture_image()

        temp, humi = fetch_temp_humi()
        print(f"   温度={temp} ℃, 湿度={humi}%")

        send_to_node_c(img, temp, humi)      # ★ 送信呼び出し
        time.sleep(10)                       # 多重撮影防止
    time.sleep(1)
