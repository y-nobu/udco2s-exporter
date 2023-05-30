from prometheus_client import start_http_server, Gauge
import random
import time
import serial
import sys
import re

# ud-co2s の出力から値を取り出す
# 出力は b'CO2=649,HUM=41.3,TMP=27.0\r\n' のような形式
def extract_udco2s_values(string):
    pattern = rb'CO2=(\d+),HUM=(\d+\.\d+),TMP=(\d+\.\d+)'
    matches = re.findall(pattern, string)
    if matches:
        values = matches[0]
        co2 = float(values[0])
        humidity = float(values[1])
        temperature = float(values[2])
        return humidity, temperature, co2
    return None

def read_udco2s_value(ser):
    # センサから値を取得する処理を実装
    # ser.read() などを使用してシリアルポートから値を読み取る
    # ud-co2s は STA でシリアルポートに値を出力し続ける。
    # STPで出力するのをやめる
    # とりあえず最後の値は測定値がいいなーって期待しているけど、きちんとSTP OK とか対策したほうがいいぞ
    value = ser.readlines()
    if len(value) != 0:
        humidity, temperature, co2_concentration = extract_udco2s_values(value[-1])
        return humidity, temperature, co2_concentration
    return 0, 0, 0

# PrometheusのGaugeメトリクスを定義
HUMIDITY = Gauge('humidity_percentage', 'Measured humidity percentage')
TEMPERATURE = Gauge('temperature_celsius', 'Measured temperature in Celsius')
CO2_CONCENTRATION = Gauge('co2_ppm', 'Measured CO2 concentration in parts per million')

# センサから値を読み出し、メトリクスにセットする関数
def update_metrics(ser):
    humidity, temperature, co2_concentration = read_udco2s_value(ser)
    HUMIDITY.set(humidity)
    TEMPERATURE.set(temperature)
    CO2_CONCENTRATION.set(co2_concentration)

if __name__ == '__main__':
    # 引数からシリアルポート名を取得
    if len(sys.argv) < 2:
        print("Usage: python exporter.py <serial_port>")
        sys.exit(1)
    
    serial_port = sys.argv[1]
    # init serial
    with serial.Serial(serial_port, 9600, timeout=3) as ser:
        ser.write(b"STA\r\n")
        print("Start serialport: " + serial_port)
        time.sleep(5)
        print("Start Server")
        start_http_server(8000)
        # 定期的にセンサ値を更新するループ
        while True:
            update_metrics(ser)
            time.sleep(1)
