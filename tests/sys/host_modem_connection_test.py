#!/usr/bin/env python3

"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

connection = Host.modem_conn()
print(connection)
