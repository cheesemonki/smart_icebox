from machine import  SoftI2C, Pin
from aht10_driver import AHT10

i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)

sensor = AHT10(i2c)
sensor.sensor_init()
sensor.is_calibration_enabled()


def dht11_temperature():
    sensor.read_temperature()

def dht11_humidity():
    sensor.read_humidity()