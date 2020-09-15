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
        self._ser = serial.Serial(port=self._device_identifier, baudrate=self._baud_rate, timeout=comms_timeout,
                                  parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        time.sleep(0.5)     # as GE910 - 0.3


    def close(self):
        try:
            # port...
            if self._ser:
                self._ser.close()
                self._ser = None

        finally:
            # lock...
            Lock.release(self.__lock_name)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_identifier(self):
        return self._device_identifier


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __lock_name(self):
        return self.__class__.__name__ + "-" + str(self._device_identifier).replace("/", "_")
