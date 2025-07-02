#!/usr/bin/env python3
"""
Node B  (Sense HAT 搭載 Raspberry Pi)
温度・湿度（＋気圧）を /sensor で返すだけの超軽量 API
"""

from flask import Flask, jsonify
from sense_hat import SenseHat
import subprocess

app   = Flask(__name__)
sense = SenseHat()

# ── CPU 発熱による温度誤差を簡易補正 ──────────────────────────
def _cpu_temp() -> float:
    out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    return float(out.replace("temp=", "").replace("'C\n", ""))

def get_env():
    raw_h = sense.get_temperature_from_humidity()
    raw_p = sense.get_temperature_from_pressure()
    cpu   = _cpu_temp()
    temp  = (raw_h + raw_p) / 2 - (cpu - raw_h) * 0.6   # 簡易補正
    return round(temp, 1), round(sense.get_humidity(), 1)

@app.route("/sensor", methods=["GET"])
def sensor():
    temp, humi = get_env()
    return jsonify({"temperature": temp, "humidity": humi})

if __name__ == "__main__":
    # LAN 内どこからでも呼び出せるよう 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=False)
