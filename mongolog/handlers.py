
import logging

from pprint import pprint

class MongoHandler(logging.Handler):
    def __init__(self, host='localhost', port=None, level=logging.NOTSET):
        logging.Handler.__init__(self, level)

    def emit(self,record):
        pprint(record._raw)

