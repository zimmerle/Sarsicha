#!/usr/bin/env python


from src.configuration import loadProxyConfig, Configuration
loadProxyConfig()
import getopt, sys, urllib.request

from src.logger import log
from src.database import *


def main():
    log(0, "Creating tables... " + str(Configuration().get()))
    Node.create_table()
    CommandQueue.create_table()
    PoolingLogs.create_table()
    CommandResponse.create_table()


if __name__ == "__main__":
    """
    """        
    main()

