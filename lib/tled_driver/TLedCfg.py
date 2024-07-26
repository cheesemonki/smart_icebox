 
class TLedConfig:
    def __init__(self) -> None:
        self.CS = 15    # 片选， 低电平使能
        self.RESET = 2  # 低电平复位
        self.DC = 21    # 液晶屏寄存器/数据选择信号，0：寄存器，1：数据
        self.SDI = 23   # MOSI 写
        self.SCK = 18   # 时钟
        self.LED = 4    # 背光控制，高电平点亮
        self.SDO = 19   # MISO 读
        self.T_CLK = 14 # 触摸时钟
        self.T_CS =  27 # 片选，低电平使能
        self.T_DIN = 13 # 总线输入，接MOSI
        self.T_DO  = 12 # 总线输出，接MISO
        self.T_IRQ = 33 # 中断，检测到触摸时为低电平