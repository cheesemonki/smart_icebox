from machine import SoftI2C, Pin
from aht10_driver import AHT10

class SensorController:
    def __init__(self, scl_pin=5, sda_pin=4, freq=100000):
        # 允许通过参数配置I2C引脚和频率
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        self.sensor = AHT10(self.i2c)
        self.initialize_sensor()

    def initialize_sensor(self):
        # 初始化传感器并检查是否成功
        try:
            self.sensor.sensor_init()
            if not self.sensor.is_calibration_enabled():
                # 如果校准未启用，可在此处添加提醒或处理逻辑
                print("Warning: Sensor calibration is not enabled.")
        except Exception as e:
            # 异常处理：记录或处理初始化错误
            print(f"Failed to initialize sensor: {e}")

    def read_temperature(self):
        # 封装温度读取操作，并添加异常处理
        try:
            return self.sensor.read_temperature()
        except Exception as e:
            # 在实际应用中，可以记录日志或抛出自定义异常
            print(f"Failed to read temperature: {e}")
            return None  # 或者返回一个合理的默认值或错误码

    def read_humidity(self):
        # 封装湿度读取操作，并添加异常处理
        try:
            return self.sensor.read_humidity()
        except Exception as e:
            print(f"Failed to read humidity: {e}")
            return None  # 或者返回一个合理的默认值或错误码


# 使用示例
sensor_ctrl = SensorController()
temp = sensor_ctrl.read_temperature()
humid = sensor_ctrl.read_humidity()

# 假设我们想在这里做些什么 with the readings...
print(f"Temperature: {temp} °C, Humidity: {humid}%")