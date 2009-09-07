
import logging

from pymongo.connection import Connection

class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo capped collection.
    """

    @staticmethod
    def to(db, collection, host='localhost', port=None, level=logging.NOTSET):
        return MongoHandler(Connection(host, port)[db][collection])
        
    def __init__(self, collection, level=logging.NOTSET):
        """ Init log handler and open a connection to mongo server """
        logging.Handler.__init__(self, level)
        self.collection = collection

    def emit(self,record):
        self.collection.save(record._raw)

