"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only one sampler per semaphore!

http://semanchuk.com/philip/posix_ipc/#semaphore
"""

import time

from scs_core.sync.runner import Runner

from scs_host.sync.binary_semaphore import BinarySemaphore, SignalError
from scs_host.sync.scheduler import Scheduler


# --------------------------------------------------------------------------------------------------------------------

class ScheduleRunner(Runner):
    """
    classdocs
    """

    __MIN_ACQUISITION_TIME =  0.4               # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        self.__mutex = BinarySemaphore(name, False)


    # ----------------------------------------------------------------------------------------------------------------

    def samples(self, sampler):
        checkpoint = time.time()

        while True:
            try:
                self.__mutex.acquire()

                # if acquisition too fast there is no scheduler!
                if time.time() - checkpoint > self.__MIN_ACQUISITION_TIME:
                    yield sampler.sample()

                else:
                    time.sleep(1.0)

            except SignalError:                     # SIGTERM received
                return

            finally:
                # done...
                self.__mutex.release()

                time.sleep(Scheduler.HOLD_PERIOD)
                checkpoint = time.time()


    def reset(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__mutex.name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ScheduleRunner:{mutex:%s}" % self.__mutex
