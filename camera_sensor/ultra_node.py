#!/usr/bin/env python3
"""
Node U: HC-SR04 で距離監視、閾値超過で Node S(/trigger) へ通知
"""
import time, statistics, signal, sys, requests, RPi.GPIO as GPIO

TRIG, ECHO = 15, 14
THRESHOLD_CM = 30
MEASURE_N = 3
SPD = 34300                # cm/s
NODE_S_URL = "http://192.168.137.125:5000/trigger"  # ★Node temp-hum の IP （温湿度センサー）

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

def cleanup(*_): GPIO.cleanup(); sys.exit(0)
signal.signal(signal.SIGINT, cleanup); signal.signal(signal.SIGTERM, cleanup)

def one_distance():
    GPIO.output(TRIG, 1); time.sleep(1e-5); GPIO.output(TRIG, 0)
    t0=time.time()
    while GPIO.input(ECHO)==0 and time.time()-t0<0.02: pass
    t1=time.time()
    while GPIO.input(ECHO)==1 and time.time()-t1<0.02: pass
    return (time.time()-t1)*SPD/2

get_distance = lambda: statistics.median(one_distance() for _ in range(MEASURE_N))

print("Node U 起動 – 距離監視中 …")
while True:
    d = get_distance()
    print(f"距離 {d:.1f} cm")
    if d >= THRESHOLD_CM:
        print("  しきい値超過 → Node S へ通知")
        try:
            requests.post(NODE_S_URL, json={"distance_cm": round(d,1)}, timeout=3)
        except Exception as e:
            print("通知失敗:", e)
        time.sleep(10)          # 多重トリガ抑制
    time.sleep(1)
