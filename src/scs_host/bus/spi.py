"""
Created on 4 Jul 2016

https://github.com/doceme/py-spidev
https://www.takaitra.com/spi-device-raspberry-pi/

n.b. This is currently using an unmerged PR for py-spidev
https://github.com/doceme/py-spidev/pull/130

Until this PR is merged, this PR branch should be installed into the local
python virtualenv.

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

    def __init__(self, dev_path, mode, max_speed):
        """
        Constructor
        """

        self.__dev_path = dev_path
        self.__mode = mode
        self.__max_speed = max_speed

        self.__connection = None


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        if self.__connection:
            return

        self.acquire_lock()

        self.__connection = SpiDev()
        self.__connection.open_path(self.__dev_path)

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
        return ("%s-%s" % (self.__class__.__name__, self.__dev_path)).replace('/', '_')


    # ----------------------------------------------------------------------------------------------------------------

    def xfer(self, args):
        return self.__connection.xfer(args)


    def read_bytes(self, count):
        return self.__connection.readbytes(count)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dev_path(self):
        return self.__dev_path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SPI:{dev_path:%s, mode:%d, max_speed:%d, connection:%s}" % \
               (self.__dev_path, self.__mode, self.__max_speed, self.__connection)
