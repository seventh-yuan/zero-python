_IOC_NRBITS = 8
_IOC_TYPEBITS = 8
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = ((1 << _IOC_NRBITS) - 1)
_IOC_TYPEMASK = ((1 << _IOC_TYPEBITS) - 1)
_IOC_SIZEMASK = ((1 << _IOC_SIZEBITS) - 1)
_IOC_DIRMASK = ((1 << _IOC_DIRBITS) - 1)

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = (_IOC_NRSHIFT + _IOC_NRBITS)
_IOC_SIZESHIFT = (_IOC_TYPESHIFT + _IOC_TYPEBITS)
_IOC_DIRSHIFT = (_IOC_SIZESHIFT + _IOC_SIZEBITS)


_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


IOC_IN = (_IOC_WRITE << (_IOC_DIRSHIFT))
IOC_OUT = (_IOC_READ << _IOC_DIRSHIFT)
IOC_INOUT = (_IOC_WRITE | _IOC_READ) << _IOC_SIZESHIFT
IOCSIZE_MASK = (_IOC_SIZEMASK << _IOC_SIZESHIFT)
IOCSIZE_SHIFT = _IOC_SIZESHIFT


def IOC(dir, type, nr, size):
    return ((dir << _IOC_DIRSHIFT) |
            (type << _IOC_TYPESHIFT) |
            (nr << _IOC_NRSHIFT) |
            (size << _IOC_SIZESHIFT))


def IO(type, nr):
    return IOC(_IOC_NONE, type, nr, 0)


def IOR(type, nr, size):
    return IOC(_IOC_READ, type, nr, size)


def IOW(type, nr, size):
    return IOC(_IOC_WRITE, type, nr, size)


def IOWR(type, nr, size):
    return IOC(_IOC_READ | _IOC_WRITE, type, nr, size)


def IOC_DIR(nr):
    return (nr >> _IOC_DIRSHIFT) & _IOC_DIRMASK


def IOC_TYPE(nr):
    return (nr >> _IOC_TYPESHIFT) & _IOC_TYPEMASK


def IOC_NR(nr):
    return (nr >> _IOC_NRSHIFT) & _IOC_NRMASK


def IOC_SIZE(nr):
    return ((nr >> _IOC_SIZEBITS) & _IOC_SIZEMASK)
