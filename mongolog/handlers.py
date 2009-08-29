
import logging

class MongoHandler(logging.Handler):
    def emit(self,record):
        print record

