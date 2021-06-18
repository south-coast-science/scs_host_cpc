"""
Created on 26 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A Unix domain socket abstraction, implementing ProcessComms

https://pymotw.com/2/socket/uds.html
https://gist.github.com/BenKnisley/5647884
"""

import os
import socket
import time

from scs_core.sys.process_comms import ProcessComms


# --------------------------------------------------------------------------------------------------------------------

class DomainSocket(ProcessComms):
    """
    classdocs
    """

    EOM = '\n'                              # end of message for client-server communications

    __PERMISSIONS = 0o666                   # srw-rw-rw-
    __BACKLOG = 1                           # number of unaccepted connections before refusing new connections
    __BUFFER_SIZE = 1024
    __WAIT_FOR_AVAILABILITY = 1.0           # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read(cls, connection):
        message = b''

        while True:
            data = connection.recv(cls.__BUFFER_SIZE)

            if not data:
                break

            message += data

        return message.decode()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, logger=None):
        """
        Constructor
        """
        self.__path = path                  # string
        self.__logger = logger              # Logger (for compatibility only)

        self.__socket = None                # socket.socket
        self.__conn = None


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, wait_for_availability=True):
        self.__socket = socket.socket(family=socket.AF_UNIX, type=socket.SOCK_STREAM)


    def accept(self):
        self.__socket.bind(self.path)
        self.__socket.listen(self.__BACKLOG)

        os.chmod(self.path, self.__PERMISSIONS)

        self.__conn, _ = self.__socket.accept()


    def close(self):
        if self.__socket:
            self.__socket.close()


    # ----------------------------------------------------------------------------------------------------------------
    # client-server API...

    def server_send(self, message):
        self.__send(self.__conn, message)


    def client_send(self, message):
        try:
            self.__socket.connect(self.path)
        except OSError:
            pass                    # assume that the socket is already connected

        self.__send(self.__socket, message)


    def server_receive(self):
        return self.__receive(self.__conn)


    def client_receive(self):
        return self.__receive(self.__socket)


    # ----------------------------------------------------------------------------------------------------------------

    def __send(self, channel, message):
        channel.send((message + self.EOM).encode())


    def __receive(self, channel):
        message = ''
        while True:
            char = channel.recv(1).decode()

            if char == self.EOM:
                return message

            if len(message) == self.__BUFFER_SIZE:
                raise ValueError(message)

            message += char


    # ----------------------------------------------------------------------------------------------------------------
    # unidirectional API...

    def read(self):                                             # blocking
        # socket...
        self.__socket.bind(self.path)
        self.__socket.listen(self.__BACKLOG)

        os.chmod(self.path, self.__PERMISSIONS)

        try:
            while True:
                self.__conn, _ = self.__socket.accept()

                try:
                    # data...
                    yield DomainSocket.__read(self.__conn).strip()

                finally:
                    self.__conn.close()

        finally:
            os.unlink(self.path)


    def write(self, message, wait_for_availability=True):       # message is dispatched on close()
        # socket...
        while True:
            try:
                self.__socket.connect(self.path)
                break

            except (socket.error, FileNotFoundError) as ex:
                if not wait_for_availability:
                    raise ConnectionRefusedError(ex)

                time.sleep(self.__WAIT_FOR_AVAILABILITY)

        # data...
        self.__socket.sendall(message.strip().encode())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "bbe_southern.DomainSocket:{path:%s, socket:%s}" % (self.path, self.__socket)
