#!/usr/bin/env python3
"""
Node S: /trigger で呼ばれたら温湿度を測定 → Node C(/measure) へ送信
"""
from flask import Flask, request, jsonify
from sense_hat import SenseHat
import subprocess, requests, datetime

app = Flask(__name__)
sense = SenseHat()

NODE_C_URL = "http://192.168.137.249:6000/measure"   # ★Node camera の IP （撮影用カメラ）

def cpu_temp():
    out = subprocess.check_output(["vcgencmd","measure_temp"]).decode()
    return float(out.split("=")[1].split("'")[0])

def read_env():
    t_h = sense.get_temperature_from_humidity()
    t_p = sense.get_temperature_from_pressure()
    temp = (t_h + t_p)/2 - (cpu_temp() - t_h)*0.6
    return round(temp,1), round(sense.get_humidity(),1)

@app.route("/sensor")               # デバッグ用
def sensor(): temp,hum=read_env(); return {"temperature":temp,"humidity":hum}

@app.route("/trigger", methods=["POST"])
def trigger():
    temp, hum = read_env()
    data = {"temperature": temp, "humidity": hum,
            "timestamp": datetime.datetime.now().isoformat()}
    try:
        r = requests.post(NODE_C_URL, json=data, timeout=5)
        print("▶ sent to C:", r.status_code)
    except Exception as e:
        print("送信失敗:", e)
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
