import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from obs import ObsClient, PutObjectHeader


class Watcher:
    DIRECTORY_TO_WATCH = "/path/to/your/directory"
    obs_client = None

    def __init__(self):
        self.observer = Observer()
        self.ak = os.getenv("AccessKeyID")
        self.sk = os.getenv("SecretAccessKey")
        self.security_token = os.getenv("SecurityToken")
        self.server = "https://obs.cn-north-4.myhuaweicloud.com"
        self.bucket_name = "your-bucket-name"

        # 初始化 ObsClient 一次
        if not Watcher.obs_client:
            Watcher.obs_client = ObsClient(
                access_key_id=self.ak, secret_access_key=self.sk, server=self.server
            )

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer stopped.")

        self.observer.join()

        # 关闭obsClient
        if Watcher.obs_client:
            Watcher.obs_client.close()


class Handler(FileSystemEventHandler):

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # 文件被创建
            print(f"{event.src_path} has been created!")
            # 上传文件到OBS
            self.upload_file_to_obs(event.src_path)

    def upload_file_to_obs(self, file_path):
        if Watcher.obs_client:
            object_key = os.path.basename(file_path)
            headers = PutObjectHeader()
            headers.contentType = "image/jpeg"  # 根据文件类型设置MIME类型
            metadata = {"meta1": "value1", "meta2": "value2"}  # 自定义元数据

            try:
                resp = Watcher.obs_client.putFile(
                    Watcher.obs_client.bucket_name,
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


if __name__ == "__main__":
    w = Watcher()
    w.run()
