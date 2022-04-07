# !/usr/bin/python
import os
import sys

# Logging configuration
import logging

class logger(logging.Logger):
    
    def __init__(self):
        """Initializer."""
        super().__init__()
        logging.basicConfig(filename="errlog.log",
                    filemode="a",
                    format="(%(asctime)s)  | %(name)s | %(levelname)s:%(message)s",
                    datefmt="%d  %B  %Y , %H:%M:%S",
                    level=os.environ.get("LOGLEVEL", "INFO"))
