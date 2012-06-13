
import unittest
import logging

from pymongo.connection import Connection

from os.path import dirname
from logging.config import fileConfig

class TestConfig(unittest.TestCase):
    def setUp(self):
        filename = dirname(__file__) + '/logging-test.config'
        fileConfig(filename)

        """ Create an empty database that could be used for logging """
        self.db_name = '_mongolog_test'

        self.conn = Connection('localhost')
        self.conn.drop_database(self.db_name)

    def tearDown(self):
        """ Drop used database """
        self.conn.drop_database('_mongolog_test')
        
    def testLoggingConfiguration(self):
        log = logging.getLogger('example')

        log.debug('test')
        r = self.collection.find_one({'level':'debug', 'msg':'test'})
        self.assertEquals(r['msg'], 'test')

