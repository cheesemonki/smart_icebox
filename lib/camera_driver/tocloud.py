import time
from machine import Pin, SPI
import camera
import ujson as json
from huaweicloud.obs import obs_client

# 配置摄像头引脚
camera_pin_sda = machine.Pin(26)
camera_pin_scl = machine.Pin(27)
camera_pin_xclk = machine.Pin(32)
camera_pin_pclk = machine.Pin(33)
camera_pin_vsync = machine.Pin(34)
camera_pin_href = machine.Pin(35)
camera_pin_sscb_sda = machine.Pin(36)
camera_pin_sscb_scl = machine.Pin(37)
camera_pin_reset = machine.Pin(38)

# 初始化摄像头
cam = camera.OV2640 ( 
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
    access_key_id='YOUR_ACCESS_KEY_ID',
    secret_access_key='YOUR_SECRET_ACCESS_KEY',
    endpoint='https://obs.cn-north-1.myhuaweicloud.com'  # 替换为您的Endpoint
)

# ... 定时任务部分 ...

# 上传到OBS
def upload_to_obs(image_data):
    object_name = 'image_' + time.strftime("%Y%m%d_%H%M%S") + '.jpg'
    obs_client.put_object(
        bucket_name='your-bucket-name',
        object_key=object_name,
        body=image_data
    )

def capture_and_upload():
    img = cam.capture()
    img_data = img.to_bytes(format="jpeg")

    # 上传到OBS
    upload_to_obs(img_data)