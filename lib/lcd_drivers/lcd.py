from machine import LCD, Pin
from lib.aht10_drivers.aht10 import dht11_humidity, dht11_temperature

# 初始化 LCD
lcd = LCD()
lcd.light(True)  # 打开背光

# 显示传感器数据
def show_temperature(display):
    temperature = dht11_temperature()
    display.text(f"Temp: {temperature:.1f}C", 10, 10)

def show_humidity(display):
    humidity = dht11_humidity()
    display.text(f"Humidity: {humidity:.1f}%", 10, 30)

# ... 其他显示函数

def lcd_test():
    while True:
        lcd.fill(lcd.WHITE)  # 清屏
        show_temperature(lcd)
        show_humidity(lcd)
        # ... 其他显示内容
        sleep(1)
