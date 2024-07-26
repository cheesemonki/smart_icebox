from machine import UART

def read_from_4Guart(uart_instance):
    """
    从指定的UART实例读取数据并打印。

    :param uart_instance: UART实例
    """
    # UART配置参数
    uart = UART(1, baudrate=115200, tx=17, rx=16)
    try:
        response = uart_instance.read()
        if response is not None:
            print(response.decode('utf-8'))
    except Exception as e:
        print("An error occurred:", str(e))



