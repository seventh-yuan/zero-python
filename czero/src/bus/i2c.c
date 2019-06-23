#include <bus/i2c.h>
#include <common/assert.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdlib.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <string.h>
#include <stdio.h>



i2c_t* i2c_open(const char* dev_name)
{
    ASSERT(dev_name);

    i2c_t* i2c = calloc(1, sizeof(i2c_t));
    if ((i2c->fd = open(dev_name, O_RDWR)) < 0)
        goto fail;
    i2c->dev_name = dev_name;

    if (ioctl(i2c->fd, I2C_TIMEOUT, 2) < 0)
        goto fail;
    
    if (ioctl(i2c->fd, I2C_RETRIES, 2) < 0)
        goto fail;
    
    return i2c;

fail:
    free(i2c);
    return NULL;
}

void i2c_close(i2c_t* i2c)
{
    if (i2c)
    {
        close(i2c->fd);
        i2c->fd = 0;
        free(i2c);
    }
}

int i2c_write(i2c_t* i2c, ze_u8_t addr, const ze_u8_t* wr_data, ze_size_t wr_len)
{
    ASSERT(i2c);
    ASSERT(wr_data);
    ASSERT(wr_len > 0);

    int ret = 0;
    struct i2c_rdwr_ioctl_data ioctl_data;

    ioctl_data.nmsgs = 1;
    struct i2c_msg msg;
    msg.len = wr_len;
    msg.addr = addr & 0xFF;
    msg.flags = 0;
    msg.buf = (ze_u8_t*)wr_data;
    ioctl_data.msgs = &msg;
    if ((ret = ioctl(i2c->fd, I2C_RDWR, (ze_u32_t)&ioctl_data)) < 0)
        return ret;

    return 0;
}

int i2c_read(i2c_t* i2c, ze_u8_t addr, ze_u8_t* rd_data, ze_size_t rd_len)
{
    ASSERT(i2c);
    ASSERT(rd_data);
    ASSERT(rd_len > 0);

    int ret = 0;

    struct i2c_rdwr_ioctl_data ioctl_data;

    ioctl_data.nmsgs = 1;
    struct i2c_msg msg;
    msg.len = rd_len;
    msg.addr = addr & 0xFF;
    msg.flags = I2C_M_RD;
    msg.buf = rd_data;
    ioctl_data.msgs = &msg;
    if ((ret = ioctl(i2c->fd, I2C_RDWR, (ze_u32_t)&ioctl_data)) < 0)
        return ret;

    return 0;
}

int i2c_address_write(i2c_t* i2c, ze_u8_t dev_addr, i2c_addr_t address, const ze_u8_t* wr_data, ze_size_t wr_len)
{
    ASSERT(i2c);
    ASSERT(wr_data);
    ASSERT(wr_len > 0);


    int ret = 0;
    struct i2c_rdwr_ioctl_data ioctl_data;
    ioctl_data.nmsgs = 1;
    struct i2c_msg msg;
    msg.len = wr_len + address.size;
    msg.addr = dev_addr & 0xFF;
    msg.flags = 0;
    msg.buf = calloc(wr_len + address.size, sizeof(ze_u8_t));
    memcpy(msg.buf, &address, address.size);
    memcpy(msg.buf + address.size, wr_data, wr_len);
    ioctl_data.msgs = &msg;

    if ((ret = ioctl(i2c->fd, I2C_RDWR, (ze_u32_t)&ioctl_data)) < 0)
        goto out;

    return 0;
out:
    free(msg.buf);
    return ret;
}

int i2c_address_read(i2c_t* i2c, ze_u8_t dev_addr, i2c_addr_t address, ze_u8_t* rd_data, ze_size_t rd_len)
{
    ASSERT(i2c);
    ASSERT(rd_data);
    ASSERT(rd_len > 0);

    int ret = 0;
    struct i2c_rdwr_ioctl_data ioctl_data;

    ioctl_data.nmsgs = 2;
    struct i2c_msg msgs[ioctl_data.nmsgs];
    msgs[0].len = address.size;
    msgs[0].addr = dev_addr & 0xFF;
    msgs[0].flags = 0;
    msgs[0].buf = (ze_u8_t*)&address;
    msgs[1].len = rd_len;
    msgs[1].addr = dev_addr & 0xFF;
    msgs[1].flags = I2C_M_RD;
    msgs[1].buf = rd_data;
    ioctl_data.msgs = msgs;
    if ((ret = ioctl(i2c->fd, I2C_RDWR, (ze_u32_t)&ioctl_data)) < 0)
        return ret;

    return 0;
}
