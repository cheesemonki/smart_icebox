from threading import Thread
import time
import json
from lib.camera_driver.Picamera2_Img_et import capture_and_upload, getImg, save_image
from lib.air780e_drivers._4g_uart import read_from_4Guart

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

class ThreadManager:
    def __init__(self):
        self.threads = []

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def stop_threads(self):
        pass

    def add_thread(self, name, thread_func):
        thread = Thread(target=thread_func, name=name)
        self.threads.append(thread)

    def add_capture_thread(self, interval=60):
        """Start a thread to capture and save images every `interval` seconds."""
        def capture_and_save_image(interval):
            while True:
                frame = getImg()
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f'image_{timestamp}.jpg'
                save_image(frame, filename)
                time.sleep(interval)
        self.add_thread('CaptureThread', lambda: capture_and_save_image(interval))

def main():
    thread_manager = ThreadManager()

    if IS_USE_LCD == 2:
        thread_manager.add_thread('TouchThread', touch_thread)
    elif IS_USE_LCD == 1:
        thread_manager.add_thread('LCDThread', lcd_thread)
        thread_manager.add_thread('StreamThread', stream_thread)

    thread_manager.add_thread('UARTThread', uart_thread)
    
    # Add the image capture thread with an interval of 60 seconds
    thread_manager.add_capture_thread(interval=60)
    
    thread_manager.start_threads()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()