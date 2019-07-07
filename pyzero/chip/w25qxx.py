import time
from ..zero import ZeroException


class W25QXXException(ZeroException):
    pass


class W25QXX(object):
    WRITE_ENABLE                    = 0x06,
    WRITE_DISABLE                   = 0x04,
    READ_STATUS_REGISTER1           = 0x05,
    READ_STATUS_REGISTER2           = 0X35,
    WRITE_STATUS_REGISTER           = 0x01,
    PAGE_PROGRAM                    = 0x02,
    QUAD_PAGE_PROGRAM               = 0x32,
    BLOCK_ERASE_64K                 = 0xD8,
    BLOCK_ERASE_32K                 = 0x52,
    SECTOR_ERASE                    = 0x20,
    CHIP_ERASE                      = 0xC7,

    READ_DATA                       = 0x03,

    ERASE_SUSPEND                   = 0x75,
    ERASE_RESUME                    = 0x7A,
    POWER_DOWN                      = 0xB9,
    HIGH_PERFORMANCE_MODE           = 0xA3,
    MODE_BIT_RESET                  = 0xFF,

    MANUFACTURER_DEVICE_ID          = 0x90,
    READ_UNIQUE_ID                  = 0x48,
    JEDEC_ID                        = 0x9F,

    DUMMY_DATA                      = 0x00,

    STATUS_BUSY                     = 0x01,
    STATUS_WRITE_ENABLE             = 0x02,

    SECTOR_SIZE                     = 4 * 1024,
    BLOCK32K_SIZE                   = 32 * 1024,
    BLOCK64K_SIZE                   = 64 * 1024,
    PAGE_SIZE                       = 256,

    TIMEOUT = 100 / 1000.0

    def __init__(self, spi):
        self._spi = spi

    def _read_status(self, status_id):
        return self._spi.write_then_read([status_id], 1)[0]

    def _write_enable(self):
        self._spi.write([W25QXX.WRITE_ENABLE])
        start_time = time.time()
        while time.time() - start_time < W25QXX.TIMEOUT:
            status = self._read_status(W25QXX.READ_STATUS_REGISTER1)
            if ((status & W25QXX.STATUS_BUSY) != W25QXX.STATUS_BUSY) and ((status & W25QXX.STATUS_WRITE_ENABLE) == W25QXX.STATUS_WRITE_ENABLE):
                return
            time.sleep(0.001)
        raise W25QXXException("write enable timeout!")

    def _write_disable(self):
        self._spi.write([W25QXX.WRITE_DISABLE])

    def _wait_idle(self, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout / 1000.0:
            status = self._read_status(W25QXX.READ_STATUS_REGISTER1)
            if status & W25QXX.STATUS_BUSY != W25QXX.STATUS_BUSY:
                return
            time.sleep(0.001)
        raise W25QXXException("wait idle timeout!")
    
    def _page_write(self, address, wr_data):

        self._write_enable()

        data = [W25QXX.PAGE_PROGRAM, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
        data.extend(wr_data)
        self._spi.write(data)

        self._spi._write_disable()
        
    def sector_erase(self, address):
        assert address & (W25QXX.SECTOR_SIZE - 1) == 0

        self._write_enable()

        data = [W25QXX.SECTOR_ERASE, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
        self._spi.write(data)

        self._wait_idle(W25QXX.TIMEOUT)
        self._write_disable()

    def block32_erase(self, address):
        assert address & (W25QXX.BLOCK32K_SIZE - 1) == 0

        self._write_enable()

        data = [W25QXX.BLOCK_ERASE_32K, (address >> 16) & 0xFF, (address >> 7) & 0xFF, address & 0xFF]

        self._spi.write(data)

        self._wait_idle(W25QXX.TIMEOUT)

        self._write_disable()

    def block64_erase(self, address):
        assert address & (W25QXX.BLOCK64K_SIZE - 1) == 0

        self._write_enable()

        data = [W25QXX.BLOCK_ERASE_64K, (address >> 16) & 0xFF, (address >> 7) & 0xFF, address & 0xFF]

        self._spi.write(data)

        self._wait_idle(W25QXX.TIMEOUT)

        self._write_disable()

    def write(self, address, wr_data):

        wr_len = len(wr_data)
        pos = 0
        while wr_len > 0:
            if address & (W25QXX.PAGE_SIZE - 1) + wr_len > W25QXX.PAGE_SIZE:
                length = W25QXX.PAGE_SIZE - (address & (W25QXX.PAGE_SIZE - 1))
            else:
                length = length(wr_data)
            self._page_write(address, wr_data[pos : length])
            pos += length
            wr_len -= length
            address += length

    def read(self, address, rd_len):
        data = [W25QXX.READ_DATA, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]
        return self._spi.write_then_read(data, rd_len)

    def read_manu_device_id(self):
        data = [W25QXX.MANUFACTURER_DEVICE_ID, W25QXX.DUMMY_DATA, W25QXX.DUMMY_DATA, W25QXX.DUMMY_DATA]
        rd_data = self._spi.write_then_read(data, 2)
        return (rd_data[0] << 8) | rd_data[1]