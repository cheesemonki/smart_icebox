#machine库，camera库需要下载到固件
#链接：https://pan.baidu.com/s/1FtwZfstPkn4Rsm9sRaQlIg 提取码: q1gg

from time import sleep
from lib.lcd_drivers.lcd import lcd_test
from lib.tled_driver.touch import TouchTest
from lib.camera_driver.tocloud import capture_and_upload
import _thread

# ... 其他需要的库

#   1使用显示屏 2触摸屏
IS_USE_LCD = 1
def main():

    # 自动初始化显示屏或触摸屏

    
    # 创建一个线程用于处理图片流
    def stream_thread():
        capture_and_upload();

    # 启动视频流线程
    _thread.start_new_thread(stream_thread, ())

    # 创建一个线程用于处理触摸屏
    def touch_thread():
        TouchTest()

    # 创建一个线程用于处理显示屏
    def lcd_thread():
        lcd_test()

    
    if IS_USE_LCD == 2:
        # 启动触摸屏线程
        _thread.start_new_thread(touch_thread, ())
    elif IS_USE_LCD == 1:
        # 启动显示屏线程
        _thread.start_new_thread(lcd_thread, ())

    while True: #主线程空闲
        sleep(1)

if __name__ == '__main__':
    main()
