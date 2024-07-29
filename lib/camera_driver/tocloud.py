import time
import os
import json
from machine import Pin
import camera
from huaweicloud.obs import obs_client

# 读取配置文件
def load_config(config_file_path):
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

config = load_config('../../src/config/config.json')

# 配置摄像头引脚
camera_pin_sda = Pin(26)
camera_pin_scl = Pin(27)
camera_pin_xclk = Pin(32)
camera_pin_pclk = Pin(33)
camera_pin_vsync = Pin(34)
camera_pin_href = Pin(35)
camera_pin_sscb_sda = Pin(36)
camera_pin_sscb_scl = Pin(37)
camera_pin_reset = Pin(38)

# 初始化摄像头
cam = camera.OV2640( 
    sda=camera_pin_sda,
    scl=camera_pin_scl,
    xclk=camera_pin_xclk,
    pclk=camera_pin_pclk,
    vsync=camera_pin_vsync,
    href=camera_pin_href,
    sscb_sda=camera_pin_sscb_sda,
    sscb_scl=camera_pin_sscb_scl,
    reset=camera_pin_reset
)
cam.init()

# 配置OBS客户端
obs_client = obs_client.ObsClient(
    access_key_id=config['access_key_id'],
    secret_access_key=config['secret_access_key'],
    endpoint=config['endpoint']
)

# 上传到OBS
def upload_to_obs(image_data):
    try:
        object_name = 'image_' + time.strftime("%Y%m%d_%H%M%S") + '.jpg'
        obs_client.put_object(
            bucket_name=config['bucket_name'],
            object_key=object_name,
            body=image_data
        )
    except Exception as e:
        print(f"上传到OBS失败: {e}")

def capture_and_upload():
    try:
        img = cam.capture()
        img_data = img.to_bytes(format="jpeg")
        upload_to_obs(img_data)
    except Exception as e:
        print(f"捕获图像失败: {e}")
        return
    finally:
        # 在finally块中确保摄像头资源被释放
        cam.deinit()

# 注意：如果你想在更长时间的运行中保持摄像头资源的可用性，你可以在这里重新初始化摄像头
# cam.init()
    
# 例如：
# cam.deinit()
# del cam
