
import ctypes
import argparse
import os
import fcntl
from ..zero import Zero
from ..zero import ZeroException
from ..zero import ZeroCmd
from ..zero import arg_parse

class I2CException(ZeroException):
    pass


class _CI2CMessage(ctypes.Structure):
    _fields_ = [
        ("addr", ctypes.c_ushort),
        ("flags", ctypes.c_ushort),
        ("len", ctypes.c_ushort),
        ("buf", ctypes.POINTER(ctypes.c_ubyte)),
    ]

class _CI2CIOCTransfer(ctypes.Structure):
    _fields_ = [
        ("msgs", ctypes.POINTER(_CI2CMessage)),
        ("nmsgs", ctypes.c_uint),
    ]

class I2C(object):
    _I2C_RETRIES =  0x0701
    _I2C_TIMEOUT = 0x0702
    _I2C_RDWR = 0x0707

    _I2C_M_TEN = 0x0010
    _I2C_M_RD = 0x0001
    
    def __init__(self, dev_name):
        self._fd = os.open(dev_name, os.O_RDWR)
        fcntl.ioctl(self._fd, I2C._I2C_RETRIES, 2)
        fcntl.ioctl(self._fd, I2C._I2C_TIMEOUT, 2)

    def __del__(self):
        os.close(self._fd)

    def write(self, dev_addr, wr_data, dev_ten_addr=False):
        wr_data = (ctypes.c_ubyte * len(wr_data))(*wr_data)
        ioc_transfer = _CI2CIOCTransfer()
        msg = _CI2CMessage()
        msg.buf = wr_data
        msg.len = len(wr_data)
        msg.addr = dev_addr & 0xFF
        msg.flags = I2C._I2C_M_TEN if dev_ten_addr else 0
        ioc_transfer.msgs = ctypes.pointer(msg)
        ioc_transfer.nmsgs = 1
        fcntl.ioctl(self._fd, I2C._I2C_RDWR, ioc_transfer)

    def read(self, dev_addr, rd_len, dev_ten_addr=False):
        rd_data = (ctypes.c_ubyte * rd_len)()
        ioc_transfer = _CI2CIOCTransfer()
        msg = _CI2CMessage()
        msg.buf = rd_data
        msg.len = rd_len
        msg.addr = dev_addr
        msg.flags = I2C._I2C_M_RD | (I2C._I2C_M_TEN if dev_ten_addr else 0)
        ioc_transfer.msgs = ctypes.pointer(msg)
        ioc_transfer.nmsgs = 1
        fcntl.ioctl(self._fd, I2C._I2C_RDWR, ioc_transfer)
        return list(rd_data)

    def client_write(self, dev_addr, address, wr_data, addr_size=1, dev_ten_addr=False):
        assert addr_size in [1, 2]
        data = [address & 0xFF] if addr_size == 1 else [(address >> 8) & 0xFF, address & 0xFF]
        data.extend(wr_data)
        data = (ctypes.c_ubyte * len(data))(*data)
        ioc_transfer = _CI2CIOCTransfer()
        msg = _CI2CMessage()
        msg.buf = data
        msg.len = len(data)
        msg.addr = dev_addr
        msg.flags = (I2C._I2C_M_TEN if dev_ten_addr else 0)
        ioc_transfer.msgs = ctypes.pointer(msg)
        ioc_transfer.nmsgs = 1
        fcntl.ioctl(self._fd, I2C._I2C_RDWR, ioc_transfer)
        
    def client_read(self, dev_addr, address, rd_len, addr_size=1, dev_ten_addr=False):
        assert addr_size in [1, 2]

        ioc_transfer = _CI2CIOCTransfer()
        msgs = (_CI2CMessage * 2)()
        data = [address & 0xFF] if addr_size == 1 else [(address >> 8) & 0xFF, address & 0xFF]
        msgs[0].buf = (ctypes.c_ubyte * len(data))(*data)
        msgs[0].len = len(data)
        msgs[0].addr = dev_addr
        msgs[0].flags = (I2C._I2C_M_TEN if dev_ten_addr else 0)
        rd_data = (ctypes.c_ubyte * rd_len)()
        msgs[1].buf = rd_data
        msgs[1].len = rd_len
        msgs[1].addr = dev_addr
        msgs[1].flags = I2C._I2C_M_RD | (I2C._I2C_M_TEN if dev_ten_addr else 0)
        ioc_transfer.msgs = msgs
        ioc_transfer.nmsgs = 2
        fcntl.ioctl(self._fd, I2C._I2C_RDWR, ioc_transfer)
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
    def do_client_write(self, dev_addr, address, wr_data):
        '''client_write <dev_addr> <address> <data_list>'''
        self.i2c.client_write(dev_addr, address, wr_data)

    @arg_parse
    def do_client_read(self, dev_addr, address, rd_len):
        '''client_read <dev_addr> <address> <rd_len>'''
        return self.i2c.client_read(dev_addr, address, rd_len)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help='device name')
    args = parser.parse_args()
    i2c_cmd = I2CCmd()
    i2c_cmd.i2c = I2C(args.device)
    i2c_cmd.cmdloop()