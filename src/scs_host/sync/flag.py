"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A semaphore abstraction over a filesystem.
"""

import os
import time

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class Flag(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        self.__name = name
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def raise_flag(self):
        Filesystem.mkdir(os.path.join(Host.tmp_dir(), self.name))
        self.__logger.info("raised %s" % self.name)


    def lower_flag(self):
        Filesystem.rmdir(os.path.join(Host.tmp_dir(), self.name))
        self.__logger.info("lowered %s" % self.name)


    def is_raised(self):
        return self.name in [file.name for file in Filesystem.ls(Host.tmp_dir())]


    def wait_for_raised(self):
        self.__logger.info("waiting for %s..." % self.name)

        while not self.is_raised():
            time.sleep(1)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Flag:{name:%s, is_raised:%s}" % (self.name, self.is_raised())
