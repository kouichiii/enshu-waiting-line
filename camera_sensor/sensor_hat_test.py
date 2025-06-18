import smbus2
import bme280

port = 1
address = 0x76  # または 0x77（i2cdetect -y 1 で確認）
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)

print(f"🌡 温度: {data.temperature:.2f} °C")
print(f"💧 湿度: {data.humidity:.2f} %")
print(f"📈 気圧: {data.pressure:.2f} hPa")
