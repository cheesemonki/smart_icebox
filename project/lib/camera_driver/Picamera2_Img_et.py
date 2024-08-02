 

class Imget:
    def __init__(self):
        # 创建一个Picamera2对象的实例
        self.cam = Picamera2()

        # 设置相机预览的分辨率
        self.cam.preview_configuration.main.size = (640, 360)
        self.cam.preview_configuration.main.format = "RGB888"
        # 设置预览帧率
        self.cam.preview_configuration.controls.FrameRate = 50
        # 对预览帧进行校准
        self.cam.preview_configuration.align()
        # 配置相机为预览模式
        self.cam.configure("preview")
        # 设置相机控制参数为连续对焦模式(自动对焦)
        self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        # 启动相机
        self.cam.start()

    def getImg(self):
        # 获取相机捕获的图像数组(numpy数组)
        frame = self.cam.capture_array()
        # 返回捕获的图像数组
        return frame

    def save_image(self, frame, filename='image.jpg'):
        # 将numpy数组转换为PIL图像对象
        img = Image.fromarray(frame)
        # 保存图像到指定文件
        img.save(filename)

    def __del__(self):
        self.cam.stop()
        self.cam.close()