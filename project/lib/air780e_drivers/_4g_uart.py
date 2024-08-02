import serial

def read_from_4Guart(port='/dev/ttyS0', baudrate=115200):
    """
    从指定的串口读取数据并打印。

    :param port: 串口设备名，默认为'/dev/ttyS0'
    :param baudrate: 波特率，默认为115200
    """
    try:
        # 创建串口对象
        uart_instance = serial.Serial(port, baudrate=baudrate)
        response = uart_instance.readline()  # 读取一行数据
        if response:
            print(response.decode('utf-8'))  # 打印解码后的数据
    except Exception as e:
        print("An error occurred:", str(e))