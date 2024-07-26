from lib.tled_driver.ili9341 import Display, color565
from lib.tled_driver.xpt2046 import Touch
from machine import Pin, SPI, idle
from lib.tled_driver.TLedCfg import TLedConfig
from time import sleep
from lib.aht10_drivers.aht10 import  dht11_humidity, dht11_temperature

# 显示传感器数据
def show_temperature(display):
    temperature = dht11_temperature()  # 获取温度数据
    display.draw_text8x8(10, 10, f"Temp: {temperature:.1f}C", color565(255, 255, 255))

def show_humidity(display):
    humidity = dht11_humidity()  # 获取湿度数据
    display.draw_text8x8(10, 30, f"Humidity: {humidity:.1f}%", color565(255, 255, 255))

def show_status(display):
    display.draw_text8x8(10, 50, "Status: Normal", color565(0, 255, 0))

def show_inventory(display):
    display.draw_text8x8(10, 70, "Items: 10", color565(255, 255, 255))

def show_settings(display):
    display.draw_text8x8(10, 90, "Settings Menu", color565(255, 255, 255))

def show_alert(display):
    display.draw_text8x8(10, 110, "Alert: Door Open", color565(255, 0, 0))

class Demo(object):
    """Touchscreen simple demo."""

    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)
    GREEN = color565(0, 255, 0)
    RED = color565(255, 0, 0)

    def __init__(self, display, spi2):
        """Initialize box.
        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        """
        ledCfg = TLedConfig()

        self.display = display
        self.touch = Touch(
            spi2,
            cs=Pin(ledCfg.T_CS),
            int_pin=Pin(ledCfg.T_IRQ),
            int_handler=self.touchscreen_press,
        )
        self.display.clear(color565(0, 0, 0))  # Clear screen with black color

    def touchscreen_press(self, x, y):
        """Process touchscreen press events."""
        print("Touch at coordinates ({}, {})".format(x, y))

        # Simple touch areas
        if 10 <= x <= 100 and 10 <= y <= 30:
            self.display.clear()
            show_temperature(self.display)
        elif 10 <= x <= 100 and 30 <= y <= 50:
            self.display.clear()
            show_humidity(self.display)
        elif 10 <= x <= 100 and 50 <= y <= 70:
            self.display.clear()
            show_status(self.display)
        elif 10 <= x <= 100 and 70 <= y <= 90:
            self.display.clear()
            show_inventory(self.display)
        elif 10 <= x <= 100 and 90 <= y <= 110:
            self.display.clear()
            show_settings(self.display)
        elif 10 <= x <= 100 and 110 <= y <= 130:
            self.display.clear()
            show_alert(self.display)

def TouchTest():
    """Test code."""
    ledCfg = TLedConfig()
    power = Pin(ledCfg.LED, Pin.OUT)
    power.value(1)
    
    spi1 = SPI(2, baudrate=32000000, sck=Pin(ledCfg.SCK), mosi=Pin(ledCfg.SDI))
    spi2 = SPI(1, baudrate=1000000, sck=Pin(ledCfg.T_CLK), mosi=Pin(ledCfg.T_DIN))
    display = Display(spi1, dc=Pin(ledCfg.DC), cs=Pin(ledCfg.CS), rst=Pin(ledCfg.RESET))

    demo = Demo(display, spi2)

    try:
        while True:
            idle()
    except KeyboardInterrupt:
        print("\nCtrl-C pressed. Cleaning up and exiting...")
    finally:
        display.cleanup()
