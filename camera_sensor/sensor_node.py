import socket
import time
from datetime import datetime

# 通信設定
CAMERA_IP = '192.168.0.100'  # カメラ端末のIPアドレス
CAMERA_PORT = 9000           # カメラがトリガーを受け付けるポート
SENSOR_HOST = '0.0.0.0'      # 自端末の待機アドレス
SENSOR_PORT = 9100           # 自端末が画像を受信するポート

SAVE_DIR = "./received_images"

def send_trigger_to_camera():
    """カメラ端末にトリガーを送信する"""
    with socket.socket() as sock:
        sock.connect((CAMERA_IP, CAMERA_PORT))
        sock.sendall(b'trigger')
    print("[SENSOR-DEMO] Trigger sent to camera")

def receive_image_from_camera():
    """画像を受信してファイルに保存"""
    with socket.socket() as server:
        server.bind((SENSOR_HOST, SENSOR_PORT))
        server.listen(1)
        print(f"[SENSOR-DEMO] Listening on {SENSOR_HOST}:{SENSOR_PORT} for image...")
        conn, addr = server.accept()
        with conn:
            print(f"[SENSOR-DEMO] Receiving image from {addr}")
            data_len = int.from_bytes(conn.recv(8), 'big')
            image_data = b''
            while len(image_data) < data_len:
                packet = conn.recv(4096)
                if not packet:
                    break
                image_data += packet

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{SAVE_DIR}/image_{timestamp}.jpg"
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"[SENSOR-DEMO] Image saved: {filename}")

def main():
    import os
    os.makedirs(SAVE_DIR, exist_ok=True)
    
    # 1. トリガー送信
    send_trigger_to_camera()
    # 2. 画像受信
    receive_image_from_camera()

if __name__ == '__main__':
    main()
