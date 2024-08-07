import os
import time
from PIL import Image
import numpy as np
from picamera2 import Picamera2, Preview
from obs import ObsClient, PutObjectHeader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Imget:
    def __init__(self):
        # 创建一个Picamera2对象的实例
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (640, 360)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.controls.FrameRate = 50
        self.cam.preview_configuration.align()
        self.cam.configure("preview")
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        self.cam.start()

    def get_img(self):
        # 获取相机捕获的图像数组(numpy数组)
        frame = self.cam.capture_array()
        return frame

    def save_image(self, frame, filename='image.jpg'):
        # 将numpy数组转换为PIL图像对象并保存
        img = Image.fromarray(frame)
        img.save(filename)
        return filename

    def __del__(self):
        self.cam.stop()
        self.cam.close()


class CameraToCloud:
    def __init__(self):
        self.imget = Imget()
        self.ak = os.getenv("AccessKeyID")
        self.sk = os.getenv("SecretAccessKey")
        self.security_token = os.getenv("SecurityToken")
        self.server = "https://obs.cn-north-4.myhuaweicloud.com"
        self.bucket_name = "your-bucket-name"
        self.obs_client = ObsClient(
            access_key_id=self.ak, secret_access_key=self.sk, server=self.server
        )

    def capture_and_save(self):
        frame = self.imget.get_img()
        filename = self.imget.save_image(frame)
        return filename

    def upload_to_obs(self, file_path):
        if self.obs_client:
            object_key = os.path.basename(file_path)
            headers = PutObjectHeader()
            headers.contentType = "image/jpeg"  # 根据文件类型设置MIME类型
            metadata = {"meta1": "value1", "meta2": "value2"}  # 自定义元数据

            try:
                resp = self.obs_client.putFile(
                    self.bucket_name,
                    object_key,
                    file_path,
                    metadata,
                    headers,
                )
                if resp.status < 300:
                    print(f"Upload of {file_path} to OBS succeeded.")
                    print("Request ID:", resp.requestId)
                    print("ETag:", resp.body.etag)
                    print("Version ID:", resp.body.versionId)
                    print("Storage Class:", resp.body.storageClass)
                else:
                    print(
                        f"Upload of {file_path} to OBS failed: {resp.errorCode} - {resp.errorMessage}"
                    )
            except Exception as e:
                print(f"An error occurred while uploading {file_path}: {str(e)}")

    def capture_and_upload(self):
        file_path = self.capture_and_save()
        self.upload_to_obs(file_path)

    # 获取对象数据
def get_object_data(token, bucket_name, object_name):
    url = f"https://{bucket_name}.obs.cn-north-4.myhuaweicloud.com/{object_name}"
    headers = {
        "Authorization": f"OBS {token}",
        "Date": "current_date"  # 替换为当前日期
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to get object data: {response.status_code}")

    def __del__(self):
        if self.obs_client:
            self.obs_client.close()


if __name__ == "__main__":
    camera_to_cloud = CameraToCloud()
    try:
        while True:
            camera_to_cloud.capture_and_upload()
            time.sleep(10)  # 每10秒拍摄并上传一次
    except KeyboardInterrupt:
        print("Program interrupted.")
