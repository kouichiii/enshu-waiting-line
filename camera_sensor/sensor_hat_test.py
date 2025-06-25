#!/usr/bin/env python3
from sense_hat import SenseHat
import time

sense = SenseHat()

def test_environment():
    print("\n🌡️ 環境センサー (温度 / 湿度 / 気圧)")
    temp_h = sense.get_temperature_from_humidity()
    temp_p = sense.get_temperature_from_pressure()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    print(f"温度(湿度センサー由来): {temp_h:.2f} ℃")
    print(f"温度(気圧センサー由来): {temp_p:.2f} ℃")
    print(f"湿度: {humidity:.2f} %")
    print(f"気圧: {pressure:.2f} hPa")

def test_motion():
    print("\n🌀 モーションセンサー (加速度 / ジャイロ / 磁気)")
    accel = sense.get_accelerometer_raw()
    gyro = sense.get_gyroscope_raw()
    mag = sense.get_compass_raw()
    orientation = sense.get_orientation()
    print(f"加速度 X:{accel['x']:.3f} Y:{accel['y']:.3f} Z:{accel['z']:.3f}")
    print(f"ジャイロ X:{gyro['x']:.3f} Y:{gyro['y']:.3f} Z:{gyro['z']:.3f}")
    print(f"地磁気 X:{mag['x']:.3f} Y:{mag['y']:.3f} Z:{mag['z']:.3f}")
    print(f"方位: Yaw={orientation['yaw']:.2f}°, Pitch={orientation['pitch']:.2f}°, Roll={orientation['roll']:.2f}°")

def test_led_matrix():
    print("\n💡 LED マトリクス表示テスト")
    sense.show_message("TEST OK", scroll_speed=0.05, text_colour=[0, 255, 0])
    time.sleep(1)
    sense.clear()

def test_joystick():
    print("\n🎮 ジョイスティック動作確認（5秒間）")
    print("動かしてみてください…")
    start_time = time.time()
    while time.time() - start_time < 5:
        for event in sense.stick.get_events():
            print(f"方向: {event.direction}, 状態: {event.action}")
        time.sleep(0.1)

def main():
    print("=== Sense HAT 総合テスト ===")
    test_environment()
    test_motion()
    test_led_matrix()
    test_joystick()
    print("\n✅ テスト完了！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sense.clear()
        print("\n⛔ テスト中断されました")
