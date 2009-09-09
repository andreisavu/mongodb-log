
import unittest
import logging

from pymongo.connection import Connection

from mongolog.handlers import MongoHandler

class TestHandler(unittest.TestCase):

    def setUp(self):
        """ Create an empty database that could be used for logging """
        self.db_name = '_mongolog_test'

        self.conn = Connection('localhost')
        self.conn.drop_database(self.db_name)

        self.db = self.conn[self.db_name]
        self.collection = self.db['log']

    def tearDown(self):
        """ Drop used database """
        self.conn.drop_database('_mongolog_test')
        

    def testLogging(self):
        """ Simple logging example """
        log = logging.getLogger('example')
        log.setLevel(logging.DEBUG)

        log.addHandler(MongoHandler(self.collection))

        log.debug('test')

        r = self.collection.find_one({'level':'debug', 'msg':'test'})
        self.assertEquals(r['msg'], 'test')


