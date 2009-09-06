
import logging

from pymongo.connection import Connection
from pprint import pprint

class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo capped collection.
    """

    def __init__(self, db, collection, host='localhost', port=None,level=logging.NOTSET):
        """ Init log handler and open a connection to mongo server """
        logging.Handler.__init__(self, level)
        self.conn = Connection(host=host, port=port)
        self.db = self.conn[db]
        self.collection = self.db[collection]
        

    def emit(self,record):
        self.collection.save(record._raw)

