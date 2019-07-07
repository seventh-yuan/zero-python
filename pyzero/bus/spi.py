
import ctypes
import argparse
import os
import fcntl
import array
from .. import ioc
from ..zero import ZeroException
from ..zero import ZeroCmd
from ..zero import arg_parse


class SPIException(ZeroException):
    pass


class _CSPIIOCTransfer(ctypes.Structure):
    _fields_ = [
        ("tx_buf", ctypes.c_uint64),
        ("rx_buf", ctypes.c_uint64),
        ("len", ctypes.c_uint32),
        ("speed_hz", ctypes.c_uint32),
        ("delay_usecs", ctypes.c_uint16),
        ("bits_per_word", ctypes.c_uint8),
        ("cs_change", ctypes.c_uint8),
        ("pad", ctypes.c_uint32),
    ]


class SPI(object):
    _SPI_CPHA = 0x01
    _SPI_CPOL = 0x02
    _SPI_MODE_0 = (0 | 0)
    _SPI_MODE_1 = (0 | _SPI_CPHA)
    _SPI_MODE_2 = (_SPI_CPOL | 0)
    _SPI_MODE_3 = (_SPI_CPOL | _SPI_CPHA)

    _SPI_IOC_MAGIC = ord('k')

    _SPI_IOC_WR_MODE = ioc.IOW(_SPI_IOC_MAGIC, 1, 1)
    _SPI_IOC_RD_MODE = ioc.IOR(_SPI_IOC_MAGIC, 1, 1)
    _SPI_IOC_WR_MAX_SPEED_HZ = ioc.IOW(_SPI_IOC_MAGIC, 4, 4)
    _SPI_IOC_RD_MAX_SPEED_HZ = ioc.IOR(_SPI_IOC_MAGIC, 4, 4)
    _SPI_IOC_WR_BITS_PER_WORD = ioc.IOW(_SPI_IOC_MAGIC, 3, 1)
    _SPI_IOC_RD_BITS_PER_WORD = ioc.IOR(_SPI_IOC_MAGIC, 3, 1)

    def __init__(self, dev_name):
        self._fd = os.open(dev_name, os.O_RDWR)

    def __del__(self):
        os.close(self._fd)

    def _spi_msgsize(self, n):
        return 32 * n

    def _spi_ioc_message(self, n):
        return ioc.IOW(SPI._SPI_IOC_MAGIC, 0, self._spi_msgsize(n))

    def set_speed(self, speed_hz):
        buf = array.array('I', [speed_hz])
        fcntl.ioctl(self._fd, SPI._SPI_IOC_WR_MAX_SPEED_HZ, buf)

    def get_speed(self):
        buf = array.array('I', [0])
        fcntl.ioctl(self._fd, SPI._SPI_IOC_RD_MAX_SPEED_HZ, buf)
        return buf[0]

    def set_mode(self, mode):
        mode = array.array('B', [mode])
        fcntl.ioctl(self._fd, SPI._SPI_IOC_WR_MODE, mode)

    def get_mode(self):
        mode = array.array('B', [0])
        fcntl.ioctl(self._fd, SPI._SPI_IOC_RD_MODE, mode)
        return mode[0]

    def write(self, wr_data):
        ioc_transfer = _CSPIIOCTransfer()
        buf = array.array('B', wr_data)
        buf_addr, buf_len = buf.buffer_info()
        ioc_transfer.tx_buf = buf_addr
        ioc_transfer.len = buf_len
        fcntl.ioctl(self._fd, self._spi_ioc_message(1), ioc_transfer)

    def read(self, rd_len):
        ioc_transfer = _CSPIIOCTransfer()
        buf = array.array('B', [0 for i in range(rd_len)])
        buf_addr, buf_len = buf.buffer_info()
        ioc_transfer.rx_buf = buf_addr
        ioc_transfer.len = buf_len
        fcntl.ioctl(self._fd, self._spi_ioc_message(1), ioc_transfer)
        return buf.tolist()

    def write_and_read(self, wr_data):
        ioc_transfer = _CSPIIOCTransfer()
        tx_buf = array.array('B', wr_data)
        tx_buf_addr, tx_len = tx_buf.buffer_info()
        rx_buf = array.array('B', [0 for i in range(len(wr_data))])
        rx_buf_addr = rx_buf.buffer_info()[0]
        ioc_transfer.tx_buf = tx_buf_addr
        ioc_transfer.rx_buf = rx_buf_addr
        ioc_transfer.len = tx_len
        fcntl.ioctl(self._fd, self._spi_ioc_message(1), ioc_transfer)
        return rx_buf.tolist()

    def write_then_read(self, wr_data, rd_len):
        ioc_transfer = (_CSPIIOCTransfer * 2)()
        tx_buf = array.array('B', wr_data)
        tx_buf_addr, tx_len = tx_buf.buffer_info()
        rx_buf = array.array('B', [0 for i in range(rd_len)])
        rx_buf_addr, rx_len = rx_buf.buffer_info()
        ioc_transfer[0].tx_buf = tx_buf_addr
        ioc_transfer[0].len = tx_len
        ioc_transfer[1].rx_buf = rx_buf_addr
        ioc_transfer[1].len = rx_len
        fcntl.ioctl(self._fd, self._spi_ioc_message(2), ioc_transfer)
        return rx_buf.tolist()

class SPICmd(ZeroCmd):
    intro = 'Welcome to SPI shell. Type help or ? to list the command'
    prompt = 'spi>>'

    @arg_parse
    def do_get_speed(self):
        '''get_speed'''
        return self.spi.get_speed()

    @arg_parse
    def do_set_speed(self, speed):
        '''set_speed speed_hz'''
        self.spi.set_speed(speed)

    @arg_parse
    def do_get_mode(self):
        '''get_mode'''
        return self.spi.get_mode()

    @arg_parse
    def do_set_mode(self, mode):
        '''set_mode mode'''
        self.spi.set_mode(mode)

    @arg_parse
    def do_write(self, wr_data):
        '''write <data list>'''
        self.spi.write(wr_data)

    @arg_parse
    def do_read(self, rd_len):
        '''read <rd_len>'''
        return self.spi.read(rd_len)

    @arg_parse
    def do_write_and_read(self, wr_data):
        '''write_and_read <data_list>'''
        self.spi.write_and_read(wr_data)

    @arg_parse
    def do_write_then_read(self, wr_data, wr_len):
        '''client_read <dev_addr> <address> <rd_len>'''
        return self.spi.write_then_read(wr_data, wr_len)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', help='device name')
    args = parser.parse_args()
    i2c_cmd = SPICmd()
    i2c_cmd.spi = SPI(args.device)
    i2c_cmd.cmdloop()