"""
Created on 27 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stdio abstraction, implementing ProcessComms
"""

import os
import readline
import sys
import termios

from scs_core.sys.process_comms import ProcessComms


# --------------------------------------------------------------------------------------------------------------------

class StdIO(ProcessComms):
    """
    classdocs
    """

    __HISTORY_LENGTH =  100
    __VOCABULARY = []
    __READLINE_COMPLETION = 'tab: complete'

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def prompt(prompt_str):
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
        except termios.error:
            pass

        line = input(prompt_str).strip()

        return line.strip()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def set(cls, vocabulary=(), history_filename=None):
        # completion...
        cls.__VOCABULARY = vocabulary

        readline.parse_and_bind(cls.__READLINE_COMPLETION)
        readline.set_completer(cls.completer)

        # history...
        if history_filename:
            cls.load_history(history_filename)


    @classmethod
    def clear(cls):
        cls.__VOCABULARY = ()
        readline.set_completer()

        readline.clear_history()


    @classmethod
    def completer(cls, text, state):
        results = [token for token in cls.__VOCABULARY if token.startswith(text)]

        return results[state]


    @classmethod
    def load_history(cls, filename):
        if os.path.exists(filename):
            readline.read_history_file(filename)


    @classmethod
    def save_history(cls, filename):
        readline.set_history_length(cls.__HISTORY_LENGTH)
        readline.write_history_file(filename)


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
