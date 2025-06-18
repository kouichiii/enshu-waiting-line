#!/usr/bin/env python3
# Note:
# DS18B20's data pin must be connected to GPIO4 (pin 7).
# Reads temperature from sensor and prints to stdout

import os
import time

def readSensor(sensor_id):
    try:
        with open(f"/sys/bus/w1/devices/{sensor_id}/w1_slave", "r") as tfile:
            lines = tfile.readlines()
            if lines[0].strip()[-3:] != "YES":
                print(f"Sensor {sensor_id} not ready")
                return
            temperature_data = lines[1].split("t=")
            if len(temperature_data) == 2:
                temperature = float(temperature_data[1]) / 1000
                print(f"Sensor: {sensor_id} - Current temperature : {temperature:.3f} °C")
    except FileNotFoundError:
        print(f"Sensor {sensor_id} not found")

def readSensors():
    sensor_found = False
    base_dir = "/sys/bus/w1/devices/"
    for device in os.listdir(base_dir):
        if device.startswith("28-"):
            readSensor(device)
            sensor_found = True
    if not sensor_found:
        print("No sensor found! Check connection.")

def loop():
    while True:
        readSensors()
        time.sleep(1)

def destroy():
    pass  # Nothing to cleanup

# Main
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        print("\nProgram terminated by user.")
