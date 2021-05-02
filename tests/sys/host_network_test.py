#!/usr/bin/env python3

"""
Created on 2 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

networks = Host.networks()
print(networks)
