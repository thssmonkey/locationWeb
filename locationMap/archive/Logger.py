#!/usr/bin/env python3.6

import sys
import logging

class Logger:
    """Custom logger"""
    def __init__(self, name, logfile=None, level=logging.DEBUG):
        ####################################  Config logging  ########################################
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(f'{name}')

        self.logger.setLevel(level)

        logfile = logfile if logfile else './TeamMaker.log'
        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)
        ##############################################################################################

    def get_logger(self):
        return self.logger
