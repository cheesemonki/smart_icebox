import time
import smbus
import struct

AHT10_ADDR = const(0x38)
AHT10_CALIBRATION_CMD = const(0xE1)         # calibration cmd for measuring
AHT10_NORMAL_CMD = const(0xA8)         # normal cmd
AHT10_GET_DATA = const(0xAC)         # get data cmd

class AHT10:
    """Class which provides interface to AHT10 temperature and humidity sensor."""
    def __init__(self, bus_num=1, address=0x38):
        self.bus = smbus.SMBus(bus_num)
        self.address = address

    def sensor_init(self):
        buf = bytearray([0x00, 0x00])
        self.bus.write_i2c_block_data(self.address, AHT10_NORMAL_CMD, buf)
        time.sleep(0.350)
        buf[0] = 0x08
        self.bus.write_i2c_block_data(self.address, AHT10_CALIBRATION_CMD, buf)
        time.sleep(0.450)

    def is_calibration_enabled(self):
        status = self.bus.read_byte(self.address)
        if status & 0x68 == 0x08:
            return True
        else:
            return False

    def read_temperature(self):
        cmd = bytearray([0x00, 0x00])
        self.bus.write_i2c_block_data(self.address, AHT10_GET_DATA, cmd)

        if self.is_calibration_enabled():
            temp = self.bus.read_i2c_block_data(self.address, 0, 6)
            temp_hex = struct.unpack(">BBBBBB", bytes(temp))
            cur_temp = ((temp_hex[3] & 0xf) << 16 | temp_hex[4] << 8 | temp_hex[5]) * 200.0 / (1 << 20) - 50
            return cur_temp
        else:
            self.sensor_init()
            print("The AHT10 is under an abnormal status. Please try again")

    def read_humidity(self):
        cmd = bytearray([0x00, 0x00])
        self.bus.write_i2c_block_data(self.address, AHT10_GET_DATA, cmd)

        if self.is_calibration_enabled():
            temp = self.bus.read_i2c_block_data(self.address, 0, 6)
            temp_hex = struct.unpack(">BBBBBB", bytes(temp))

            while temp_hex[2] == 0:
                temp = self.bus.read_i2c_block_data(self.address, 0, 6)
                temp_hex = struct.unpack(">BBBBBB", bytes(temp))

            cur_humi = (temp_hex[1] << 12 | temp_hex[2] << 4 | (temp_hex[3] & 0xf0) >> 4) * 100.0 / (1 << 20)
            return cur_humi
        else:
            self.sensor_init()
            print("The AHT10 is under an abnormal status. Please try again")