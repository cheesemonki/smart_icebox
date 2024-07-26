#machine库，camera库需要下载到固件
#链接：https://pan.baidu.com/s/1FtwZfstPkn4Rsm9sRaQlIg 提取码: q1gg
from machine import Pin, SPI
import camera

from time import sleep
from lib.tled_driver.touch import TouchTest
from lib.camera_driver.tocloud import capture_and_upload
import _thread

# ... 其他需要的库

def main():

    # 自动初始化显示屏和触摸屏

    
    # 创建一个线程用于处理图片流
    def stream_thread():
        capture_and_upload();

    # 启动视频流线程
    _thread.start_new_thread(stream_thread, ())

    # 创建一个线程用于处理触摸屏
    def touch_thread():
        TouchTest()

    # 启动视频流线程
    _thread.start_new_thread(touch_thread, ())

    while True: #主线程空闲
        sleep(1)

if __name__ == '__main__':
    main()
