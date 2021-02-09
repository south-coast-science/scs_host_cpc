"""
Created on 27 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stdio abstraction, implementing ProcessComms
"""

import sys
import termios

from scs_core.sys.process_comms import ProcessComms


# --------------------------------------------------------------------------------------------------------------------

class StdIO(ProcessComms):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def prompt(prompt_str):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        print(prompt_str, end="", file=sys.stderr)
        line = input().strip()

        return line.strip()


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, wait_for_availability=True):
        pass


    def close(self):
        sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def read(self):
        for line in sys.stdin:
            yield line.strip()


    def write(self, message, wait_for_availability=True):       # message should be flushed on close
        print(message.strip())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StdIO:{}"
