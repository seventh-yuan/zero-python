import ctypes
import argparse
from ..zero import Zero
from ..zero import ZeroException
from ..zero import ZeroCmd
from ..zero import arg_parse

class I2CException(ZeroException):
    pass


def I2CMakeAddr(addr, size):
    return (addr | size << 30)


def I2CGetAddrLen(addr):
    return (addr >> 30)


class I2C(Zero):

    def __init__(self, dev_name):
        self._dev_name = dev_name
        self.cpointer = self.base_lib.i2c_open(dev_name)
    
    def __del__(self):
        self.base_lib.i2c_close(self.cpointer)

    def write(self, addr, wr_data):
        ret = self.base_lib.i2c_write(self.cpointer, addr, (ctypes.c_ubyte * len(wr_data))(*wr_data), len(wr_data))
        if ret != 0:
            raise I2CException("write data to 0x{:02x} failed.".format(addr))

    def read(self, addr, rd_len):
        rd_data = (ctypes.c_ubyte * rd_len)()
        ret = self.base_lib.i2c_read(self.cpointer, addr, rd_data, rd_len)
        if ret != 0:
            raise I2CException("Read data from 0x{:02x} failed.".format(addr))
        return list(rd_data)

    def address_write(self, dev_addr, address, wr_data):
        ret = self.base_lib.i2c_address_write(self.cpointer, dev_addr, I2CMakeAddr(address, 1), (ctypes.c_ubyte * len(wr_data))(*wr_data), len(wr_data))
        if ret != 0:
            raise I2CException("address write to 0x{:02x} failed.".format(dev_addr))

    def address_read(self, dev_addr, address, rd_len):
        rd_data = (ctypes.c_ubyte * rd_len)()
        ret = self.base_lib.i2c_address_read(self.cpointer, dev_addr, I2CMakeAddr(address, 1), rd_data, rd_len)
        if ret != 0:
            raise I2CException("address read from 0x{:02x} failed.".format(dev_addr))
        return list(rd_data)


class I2CCmd(ZeroCmd):
    intro = 'Welcome to I2C shell. Type help or ? to list the command'
    prompt = 'i2c>>'

    @arg_parse
    def do_write(self, addr, wr_data):
        '''write <addr> <data list>'''
        self.i2c.write(addr, wr_data)

    @arg_parse
    def do_read(self, addr, rd_len):
        '''read <addr> <rd_len>'''
        return self.i2c.read(addr, rd_len)

    @arg_parse
    def do_address_write(self, dev_addr, address, addr_len, wr_data):
        '''address_write <dev_addr> <address> <addr_len> <data_list>'''
        self.i2c.address_write(dev_addr, I2CMakeAddr(address, addr_len), wr_data)

    @arg_parse
    def do_address_read(self, dev_addr, address, addr_len, rd_len):
        '''address_read <dev_addr> <address> <addr_len> <rd_len>'''
        return self.i2c.address_read(dev_addr, I2CMakeAddr(address, addr_len), rd_len)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help='device name')
    args = parser.parse_args()
    i2c_cmd = I2CCmd()
    i2c_cmd.i2c = I2C(args.device)
    i2c_cmd.cmdloop()