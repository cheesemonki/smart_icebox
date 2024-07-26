from machine import LCD, Pin
from lib.aht10_drivers.aht10 import dht11_humidity, dht11_temperature
from time import sleep

# 初始化 LCD，加入异常处理
try:
    lcd = LCD()
    lcd.light(True)  # 打开背光
except Exception as e:
    print(f"LCD初始化失败: {e}")
    raise


def show_temperature():
    try:
        temperature = dht11_temperature()
        if temperature is not None:
            lcd.text(f"Temp: {temperature:.1f}C", 10, 10)
        else:
            print("获取温度失败")
    except Exception as e:
        print(f"获取温度时发生错误: {e}")

def show_humidity():
    try:
        humidity = dht11_humidity()
        if humidity is not None and 0 <= humidity <= 100:
            lcd.text(f"Humidity: {humidity:.1f}%", 10, 30)
        else:
            print("获取湿度失败或值不在有效范围内")
    except Exception as e:
        print(f"获取湿度时发生错误: {e}")

# 主循环，引入了退出条件和更新间隔，以及对其他显示内容的预留支持
def lcd_test():
    while True:
        try:
            lcd.fill(lcd.WHITE)  # 清屏
            show_temperature()
            show_humidity()
            # 其他显示内容可以在这里添加
            sleep(10)  # 更新间隔调整为10秒
        except Exception as e:
            print(f"LCD显示循环中发生错误: {e}")
            sleep(5)
