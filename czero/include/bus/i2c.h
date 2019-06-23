#ifndef __I2C_H__
#define __I2C_H__
#include <common/types.h>

#define I2C_FLAG_BIT_ADDR_MASK  (1 << 31)
#define I2C_FLAG_7BIT_ADDR      (0 << 31)
#define I2C_FLAG_10BIT_ADDR     (1 << 31)

#define I2C_MAKE_DEV_ADDR(addr, flag)     ((i2c_dev_addr_t)(addr | flag))
#define I2C_IS_7BIT_ADDR(addr)            ((addr & I2C_FLAG_BIT_ADDR_MASK) == I2C_FLAG_7BIT_ADDR)
#define I2C_DECODE_DEV_ADDR(addr)         (addr.addr)
#define I2C_7BIT_DEV_ADDR(addr)           ((i2c_dev_addr_t)(addr | I2C_FLAG_7BIT_ADDR))

#define I2C_ADDR_SIZE_OFFSET              (30)
#define I2C_MAKE_ADDR(addr, size)         ((i2c_addr_t)((size << I2C_ADDR_SIZE_OFFSET) | addr))
#define I2C_ADDR_SIZE(addr)               (addr.size)
#define I2C_DECODE_ADDR(addr)             (addr.addr)

typedef struct {
    ze_u32_t addr           : 30;
    ze_u32_t size           : 2;
} i2c_addr_t;

typedef struct {
    const char* dev_name;
    int fd;
} i2c_t;

i2c_t* i2c_open(const char* dev_name);

void i2c_close(i2c_t* i2c);

/**
  * @brief This function is used to write data to i2c bus.
  * @param i2c: i2c bus pointer.
  * @param dev_addr: i2c device address.
  * @param data: data to be write.
  * @param len: length of data.
  * @retval 0 for success, otherwise -1.
  */
int i2c_write(i2c_t* i2c, ze_u8_t addr, const ze_u8_t* wr_data, ze_size_t wr_len);

/**
  * @brief This function is used to read data from i2c bus.
  * @param i2c: i2c bus pointer.
  * @param dev_addr: i2c device address.
  * @param data: data to be read.
  * @param len: length of data.
  * @retval 0 for success, otherwise -1.
  */
int i2c_read(i2c_t* i2c, ze_u8_t addr, ze_u8_t* rd_data, ze_size_t rd_len);

/**
  * @brief This function is used to write and read data from i2c bus.
  * @param i2c: i2c bus pointer.
  * @param dev_addr: i2c device address
  * @param address: slave device memory or register address.
  * @param flag: address option, 0 for 7 bit address, 1 for 10 bit address.
  * @param wr_data: data to be write.
  * @param wr_len: length of data to be write.
  * @retval 0 for success, otherwise -1.
  */
int i2c_address_write(i2c_t* i2c, ze_u8_t dev_addr, i2c_addr_t address, const ze_u8_t* wr_data, ze_size_t wr_len);

/**
  * @brief This function is used to write and read data from i2c bus.
  * @param i2c: i2c bus pointer.
  * @param dev_addr: i2c device address
  * @param address: slave device memory or register address.
  * @param flag: address option, 0 for 7 bit address, 1 for 10 bit address.
  * @param wr_data: data to be write.
  * @param wr_len: length of data to be read.
  * @retval 0 for success, otherwise -1.
  */
int i2c_address_read(i2c_t* i2c, ze_u8_t dev_addr, i2c_addr_t address, ze_u8_t* rd_data, ze_size_t rd_len);

#endif