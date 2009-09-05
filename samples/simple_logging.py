
import sys
sys.path.append('..')

import logging

from mongolog.handlers import MongoHandler

if __name__ == '__main__':

    log = logging.getLogger('example')
    log.setLevel(logging.DEBUG)

    log.addHandler(MongoHandler())

    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")

