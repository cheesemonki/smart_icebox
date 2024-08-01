import cv2 as cv  # 导入OpenCV库
from Picamera2_Img_et import Imget  # 自定义模块Imget中的类Imget

getImg = Imget()  # 创建Imget对象实例
while True:  # 进入循环，持续运行
    frame = getImg.getImg()  # 调用Imget对象的getImg方法获取帧图像

    cv.imshow('frame', frame)  # 在窗口中显示帧图像，窗口名称为'frame'

    if cv.waitKey(1) & 0xFF == ord('q'):  # 若按下的字符为'q'时退出循环
        break

cv.destroyAllWindows()  # 销毁所有窗口

