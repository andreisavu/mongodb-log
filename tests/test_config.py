
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
        self.collection_name = 'log_test'

        self.conn = Connection('localhost')
        self.conn.drop_database(self.db_name)

    def tearDown(self):
        """ Drop used database """
        self.conn.drop_database(self.db_name)
        
    def testLoggingConfiguration(self):
        log = logging.getLogger('example')
        log.debug('test')

        r = self.conn[self.db_name][self.collection_name]
    
        message = r.find_one({'level':'debug', 'msg':'test'})
        self.assertEquals(message['msg'], 'test')

    def testQueryableMessages(self):
        log = logging.getLogger('query')

        log.info({'address': '340 N 12th St', 'state': 'PA', 'country': 'US'})
        log.info({'address': '340 S 12th St', 'state': 'PA', 'country': 'US'})
        log.info({'address': '1234 Market St', 'state': 'PA', 'country': 'US'})

        r = self.conn[self.db_name][self.collection_name]
    
        cursor = r.find({'level':'info', 'msg.address': '340 N 12th St'})
        self.assertEquals(cursor.count(), 1, "Logger stored wrong number of"
            " messages")
        self.assertEquals(cursor[0]['msg']['address'], '340 N 12th St')

        cursor = r.find({'level':'info', 'msg.state': 'PA'})

        self.assertEquals(cursor.count(), 3, "Didn't find all three documents")
