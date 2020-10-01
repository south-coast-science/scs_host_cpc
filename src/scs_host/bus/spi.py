"""
Created on 4 Jul 2016

http://tightdev.net/SpiDev_Doc.pdf
http://www.takaitra.com/posts/492

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

/boot/uEnv.txt...
cape_disable=bone_capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN
cape_enable=bone_capemgr.enable_partno=BB-SPIDEV0,BB-SPIDEV1

chmod a+rw /sys/devices/platform/bone_capemgr/slots
"""

from spidev import SpiDev

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class SPI(object):
    """
    classdocs
    """
    __LOCK_TIMEOUT =        10.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bus, device, mode, max_speed):
        """
        Constructor
        """

        self.__bus = bus
        self.__device = device
        self.__mode = mode
        self.__max_speed = max_speed

        self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        if self.__connection:
            return

        self.acquire_lock()

        self.__connection = SpiDev()
        self.__connection.open(self.__bus, self.__device)

        self.__connection.mode = self.__mode
        self.__connection.max_speed_hz = self.__max_speed


    def close(self):
        if self.__connection is None:
            return

        self.__connection.close()
        self.__connection = None

        self.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def acquire_lock(self):
        Lock.acquire(self.__lock_name, SPI.__LOCK_TIMEOUT)


    def release_lock(self):
        Lock.release(self.__lock_name)


    @property
    def __lock_name(self):
        return "%s-%s" % (self.__class__.__name__, self.__bus)


    # ----------------------------------------------------------------------------------------------------------------

    def xfer(self, args):
        return self.__connection.xfer(args)


    def read_bytes(self, count):
        return self.__connection.readbytes(count)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bus(self):
        return self.__bus


    @property
    def device(self):
        return self.__device


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPI:{bus:%d, device:%s, mode:%d, max_speed:%d, connection:%s}" % \
               (self.__bus, self.__device, self.__mode, self.__max_speed, self.__connection)
