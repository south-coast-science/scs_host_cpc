#!/usr/bin/env python3

"""
Created on 2 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

home_path = Host.home_path()
print("home_path: %s" % home_path)

print("-")

try:
    lock_dir = Host.lock_dir()
    print("lock_dir: %s" % lock_dir)
except NotImplementedError:
    print("lock_dir: None")

try:
    tmp_dir = Host.tmp_dir()
    print("tmp_dir: %s" % tmp_dir)
except NotImplementedError:
    print("tmp_dir: None")

try:
    command_path = Host.command_path()
    print("command_path: %s" % command_path)
except NotImplementedError:
    print("command_path: None")

print("-")

scs_path = Host.scs_path()
print("scs_path: %s" % scs_path)

print("-")
