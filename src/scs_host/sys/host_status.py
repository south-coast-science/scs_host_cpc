"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class HostStatus(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, temp):
        """
        Constructor
        """
        self.__temp = Datum.float(temp, 1)          # temperature             °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return {'tmp': self.temp}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostStatus:{temp:%0.1f}" % self.temp
