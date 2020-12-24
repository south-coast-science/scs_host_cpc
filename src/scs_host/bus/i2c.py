"""
Created on 5 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://ftp.de.debian.org/debian/pool/main/i/i2c-tools/
file: i2c-tools-3.1.1/include/linux/i2c-dev.h

Change i2c bus frequency on BeagleBone Black
http://randymxj.com/?p=538
"""

import fcntl
import io
import time

from abc import ABC, abstractmethod

from scs_host.lock.lock import Lock
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class I2C(ABC):
    """
    I2C bus abstraction over UNIX /dev/i2c-n
    """
    __I2C_SLAVE =           0x0703

    __I2C_SLAVE_FORCE =     0x0706
    __I2C_TENBIT =          0x0704
    __I2C_FUNCS =           0x0705
    __I2C_RDWR =            0x0707
    __I2C_PEC =             0x0708
    __I2C_SMBUS =           0x0720

    __LOCK_TIMEOUT =        2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def fr(cls):
        pass


    @classmethod
    @abstractmethod
    def fw(cls):
        pass


    @classmethod
    @abstractmethod
    def open(cls):
        pass


    @classmethod
    @abstractmethod
    def close(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def start_tx(cls, device):
        if cls.fr() is None or cls.fw() is None:
            raise RuntimeError("cls.start_tx: bus is not open.")

        Lock.acquire(cls.__name__, cls.__LOCK_TIMEOUT)

        fcntl.ioctl(cls.fr(), cls.__I2C_SLAVE, device)
        fcntl.ioctl(cls.fw(), cls.__I2C_SLAVE, device)


    @classmethod
    def end_tx(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def read(cls, count):
        read_bytes = list(cls.fr().read(count))
        return read_bytes[0] if count == 1 else read_bytes


    @classmethod
    def read_cmd(cls, cmd, count, wait=None):
        try:
            iter(cmd)
            cls.write(*cmd)

        except TypeError:
            cls.write(cmd)

        if wait is not None:
            time.sleep(wait)

        return cls.read(count)


    @classmethod
    def read_cmd16(cls, cmd16, count, wait=None):
        cls.write16(cmd16)

        if wait is not None:
            time.sleep(wait)

        if count < 1:
            return []

        return cls.read(count)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def write(cls, *values):
        cls.fw().write(bytearray(values))


    @classmethod
    def write16(cls, *value16s):
        write_bytes = bytearray()

        for value16 in value16s:
            write_bytes += bytes([value16 >> 8])
            write_bytes += bytes([value16 & 0xff])

        cls.fw().write(write_bytes)


    @classmethod
    def write_addr(cls, addr, *values):
        cls.fw().write(bytearray([addr]) + bytes(values))


    @classmethod
    def write_addr16(cls, addr, *values):
        addr_msb = addr >> 8
        addr_lsb = addr & 0xff

        cls.fw().write(bytearray([addr_msb, addr_lsb]) + bytes(values))


# --------------------------------------------------------------------------------------------------------------------

class SensorI2C(I2C):
    """
    I2C bus abstraction over UNIX /dev/i2c-n
    """

    __FR = None
    __FW = None

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def fr(cls):
        return cls.__FR


    @classmethod
    def fw(cls):
        return cls.__FW


    @classmethod
    def open(cls):
        cls.open_for_bus(Host.I2C_SENSORS)


    @classmethod
    def open_for_bus(cls, bus):
        if cls.__FR is not None and cls.__FW is not None:
            return

        cls.__FR = io.open("/dev/i2c-%d" % bus, "rb", buffering=0)
        cls.__FW = io.open("/dev/i2c-%d" % bus, "wb", buffering=0)


    @classmethod
    def close(cls):
        if cls.__FW is not None:
            cls.__FW.close()
            cls.__FW = None

        if cls.__FR is not None:
            cls.__FR.close()
            cls.__FR = None


# --------------------------------------------------------------------------------------------------------------------

class UtilityI2C(I2C):
    """
    I2C bus abstraction over UNIX /dev/i2c-n
    """

    __FR = None
    __FW = None

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def fr(cls):
        return cls.__FR


    @classmethod
    def fw(cls):
        return cls.__FW


    @classmethod
    def open(cls):
        if cls.__FR is not None and cls.__FW is not None:
            return

        cls.__FR = io.open("/dev/i2c-%d" % Host.I2C_UTILITIES, "rb", buffering=0)
        cls.__FW = io.open("/dev/i2c-%d" % Host.I2C_UTILITIES, "wb", buffering=0)


    @classmethod
    def close(cls):
        if cls.__FW is not None:
            cls.__FW.close()
            cls.__FW = None

        if cls.__FR is not None:
            cls.__FR.close()
            cls.__FR = None


# --------------------------------------------------------------------------------------------------------------------

class EEPROMI2C(I2C):
    """
    I2C bus abstraction over UNIX /dev/i2c-n
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def fr(cls):
        return None


    @classmethod
    def fw(cls):
        return None


    @classmethod
    def open(cls):
        raise NotImplementedError


    @classmethod
    def close(cls):
        raise NotImplementedError
