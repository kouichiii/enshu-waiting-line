import socket
import os
from time import sleep

# 通信設定
CAMERA_HOST = '0.0.0.0'       # カメラが待機するアドレス
CAMERA_PORT = 9000            # センサからのトリガー受付ポート
SENSOR_IP = '192.168.0.101'   # センサ端末のIPアドレス
SENSOR_PORT = 9100            # センサが画像を受け取るポート

# デモ用画像ファイル
DEMO_IMAGE_PATH = "/home/pi/demo_images/sample.jpg"  # あらかじめ保存しておく

def send_demo_image():
    """デモ用画像をセンサに送信する"""
    if not os.path.exists(DEMO_IMAGE_PATH):
        print(f"[ERROR] Demo image not found: {DEMO_IMAGE_PATH}")
        return
    with socket.socket() as sock:
        sock.connect((SENSOR_IP, SENSOR_PORT))
        with open(DEMO_IMAGE_PATH, 'rb') as f:
            data = f.read()
            sock.sendall(len(data).to_bytes(8, 'big') + data)
    print(f"[CAMERA-DEMO] Demo image sent to sensor")

def run_demo_camera_server():
    """センサからのトリガーを待ち受けてデモ画像を送信"""
    with socket.socket() as server:
        server.bind((CAMERA_HOST, CAMERA_PORT))
        server.listen(1)
        print(f"[CAMERA-DEMO] Listening on {CAMERA_HOST}:{CAMERA_PORT} (demo mode)")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"[CAMERA-DEMO] Trigger received from {addr}")
                send_demo_image()

if __name__ == '__main__':
    run_demo_camera_server()
