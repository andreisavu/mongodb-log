
import logging

from pymongo.connection import Connection

class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo collection. This  handler is 
    designed to be used with the standard python logging mechanism.
    """

    @staticmethod
    def to(db, collection, host='localhost', port=None, level=logging.NOTSET):
        """ Create a handler for a given  """
        return MongoHandler(Connection(host, port)[db][collection])
        
    def __init__(self, collection, level=logging.NOTSET):
        """ Init log handler and store the collection handle """
        logging.Handler.__init__(self, level)
        self.collection = collection

    def emit(self,record):
        """ Store the record to the collection. Async insert """
        self.collection.save(record._raw)

