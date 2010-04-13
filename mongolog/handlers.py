
import logging

from pymongo.connection import Connection


class MongoFormatter(logging.Formatter):
    def format(self, record):
        """Format exception object as a string"""
        data = record._raw.copy()
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
        return data
    

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
        self.formatter = MongoFormatter()

    def emit(self,record):
        """ Store the record to the collection. Async insert """
        self.collection.save(self.format(record))

