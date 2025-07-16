#!/usr/bin/env python3
"""
Node C (Camera)  
  • /measure で温湿度 JSON を受け取り撮影  
  • 撮影画像＋温湿度をバックエンドへ multipart POST
"""
import datetime, cv2, requests, signal, sys
from pathlib import Path
from flask import Flask, request, jsonify

# ★ 既存パス・ID をそのまま利用
CAP_DIR = Path("/home/y-hashimoto/Documents/test/enshu-waiting-line/camera_sensor/capture") # 写真の保存先
CAP_DIR.mkdir(parents=True, exist_ok=True)

BACKEND_URL = "http://172.16.1.33:8000/api/upload"   # 送信先
DEVICE_ID   = "2"
SEND_TEST   = 0                                      # 1 なら sample2.jpg を送信

# ── カメラ初期化 ─────────────────────────────────────
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

def take_photo() -> Path:
    if SEND_TEST:
        return CAP_DIR / "sample2.jpg"

    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = CAP_DIR / f"img_{ts}.jpg"
    ok, frame = cap.read()
    if ok:
        cv2.imwrite(str(path), frame)
    else:
        print("⚠ 撮影失敗")
    return path

def send_backend(img: Path, temp, hum):
    try:
        with open(img, "rb") as f:
            files = {"image": f}
            data  = {
                "device_id":  DEVICE_ID,
                "temperature": f"{temp}",
                "humidity":   f"{hum}"
            }
            r = requests.post(BACKEND_URL, files=files, data=data, timeout=5)
        print("→ backend:", r.status_code, r.text[:80])
    except Exception as e:
        print("backend 送信例外:", e)

# ── Flask サーバ ────────────────────────────────────
app = Flask(__name__)

@app.route("/measure", methods=["POST"])
def measure():
    js = request.get_json(force=True)
    temp, hum = js.get("temperature"), js.get("humidity")
    print(f"[MEASURE] T={temp}℃ H={hum}%  → 撮影")
    img = take_photo()
    send_backend(img, temp, hum)
    return jsonify({"status": "captured"})

def cleanup(*_): cap.release(); sys.exit(0)
signal.signal(signal.SIGINT,  cleanup); signal.signal(signal.SIGTERM, cleanup)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
