#!/usr/bin/env python3

"""
Created on 24 Mar 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

report = Host.software_update_report()
print("report: %s" % report)

