"""
Created on 28 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: only one sampler per semaphore!

http://semanchuk.com/philip/posix_ipc/#semaphore
https://pymotw.com/2/multiprocessing/basics.html
"""

import sys
import time

from multiprocessing import Manager

from scs_core.sync.interval_timer import IntervalTimer
from scs_core.sync.synchronised_process import SynchronisedProcess

from scs_core.sys.logging import Logging

from scs_host.sync.binary_semaphore import BinarySemaphore, BusyError, SignalError


# --------------------------------------------------------------------------------------------------------------------

class Scheduler(object):
    """
    classdocs
    """

    RELEASE_PERIOD =                0.3             # ScheduleItem release period
    HOLD_PERIOD =                   0.6             # ScheduleRunner hold period


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, schedule, verbose=False):
        """
        Constructor
        """
        self.__schedule = schedule                  # Schedule
        self.__verbose = verbose                    # bool

        self.__jobs = []                            # array of SchedulerItem


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            for item in self.schedule.items:
                job = SchedulerItem(item, self.verbose)

                self.__jobs.append(job)
                job.start()

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def stop(self):
        for job in self.__jobs:
            job.stop()


    def join(self):
        for job in self.__jobs:
            job.join()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def schedule(self):
        return self.__schedule


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Scheduler:{schedule:%s, verbose:%s}" % (self.schedule, self.verbose)


# --------------------------------------------------------------------------------------------------------------------

class SchedulerItem(SynchronisedProcess):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, item, verbose=False):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()
        self.__logging_specification = Logging.specification()

        manager = Manager()

        SynchronisedProcess.__init__(self, manager.list())

        self._value.append(True)

        self.__item = item                                          # ScheduleItem
        self.__verbose = verbose                                    # bool

        self.__mutex = BinarySemaphore(self.item.name, True)


    # ----------------------------------------------------------------------------------------------------------------
    # SynchronisedProcess implementation...

    def stop(self):
        try:
            try:
                self.__mutex.acquire(self.item.interval)            # attempt to re-capture the mutex
            except (BusyError, SignalError):
                pass

            super().stop()

        except (ConnectionError, KeyboardInterrupt, SystemExit):
            pass


    def run(self):
        Logging.replicate(self.__logging_specification)
        self.__logger = Logging.getLogger()

        try:
            timer = IntervalTimer(self.item.interval)

            while timer.true():
                # enable sampler...
                self.__mutex.release()

                time.sleep(Scheduler.RELEASE_PERIOD)                # release period: hand semaphore to sampler

                try:
                    # disable sampler...
                    self.__mutex.acquire(self.item.interval)

                except BusyError:
                    # release...
                    self.__mutex.release()

                    self.__logger.error('%s.run: released on busy' % self.item.name)
                    sys.stderr.flush()

        except (ConnectionError, KeyboardInterrupt, SignalError, SystemExit):
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def item(self):
        return self.__item


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SchedulerItem:{item:%s, verbose:%s, mutex:%s}" % (self.item, self.verbose, self.__mutex)
