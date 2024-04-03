"""
Created on 3 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

initialise the endpoint access configuration
"""

from scs_core.aws.config.endpoint import EndpointAccess

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

EndpointAccess.init(Host)
