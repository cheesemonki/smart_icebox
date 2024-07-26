#machine库，camera库需要下载到固件
#链接：https://pan.baidu.com/s/1FtwZfstPkn4Rsm9sRaQlIg 提取码: q1gg


from lib.lcd_drivers.lcd import lcd_test
from lib.tled_driver.touch import TouchTest
from lib.camera_driver.tocloud import capture_and_upload
from lib.air780e_drivers._4g_uart import read_from_4Guart
import _thread
import time
import json

with open('../config/config.json') as f:
    config = json.load(f)
IS_USE_LCD = config.get('IS_USE_LCD', 1)

def safe_thread_function(func, name):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Error in thread '{name}': {e}")
    return wrapper

@safe_thread_function
def stream_thread():
    capture_and_upload()

@safe_thread_function
def touch_thread():
    TouchTest()

@safe_thread_function
def lcd_thread():
    lcd_test()

@safe_thread_function
def uart_thread():
    read_from_4Guart()


# 配置选项
# IS_USE_LCD = 1  # 或者从配置文件或环境变量读取

def main():
    threads = []

    if IS_USE_LCD == 2:
        threads.append(('TouchThread', touch_thread))
    elif IS_USE_LCD == 1:
        threads.extend([('LCDThread', lcd_thread), ('StreamThread', stream_thread)])

    # 新增 UART 线程
    threads.append(('UARTThread', uart_thread))
    
    for name, thread_func in threads:
        _thread.start_new_thread(thread_func, ())

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()