"""
Created on 26 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/port
"""

import serial
import time

from scs_core.sys.serial import Serial

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class HostSerial(Serial):
    """
    classdocs
    """

    __POST_OPEN_DELAY =     0.1             # seconds
    __POST_RELEASE_DELAY =  0.1             # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_path, baud_rate, hard_handshake=False):
        """
        Constructor
        """
        super().__init__(device_path, baud_rate, hard_handshake)


    # ----------------------------------------------------------------------------------------------------------------

    def open(self, lock_timeout, comms_timeout):
        # lock...
        Lock.acquire(self.__lock_name, lock_timeout)

        # port...
        self._ser = serial.Serial(port=self._device_identifier, baudrate=self._baud_rate, timeout=comms_timeout)
        time.sleep(self.__POST_OPEN_DELAY)


    def close(self):
        try:
            # port...
            if self._ser:
                self._ser.close()
                self._ser = None

        finally:
            # lock...
            Lock.release(self.__lock_name)
            time.sleep(self.__POST_RELEASE_DELAY)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_identifier(self):
        return self._device_identifier


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __lock_name(self):
        return "-".join((self.__class__.__name__, str(self._device_identifier).replace("/", "_")))
