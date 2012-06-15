import unittest
import logging

from pymongo.connection import Connection

from mongolog.handlers import MongoHandler


class TestRootLoggerHandler(unittest.TestCase):
    """
    Test Handler attached to RootLogger
    """
    def setUp(self):
        """ Create an empty database that could be used for logging """
        self.db_name = '_mongolog_test'

        self.conn = Connection('localhost')
        self.conn.drop_database(self.db_name)

        self.db = self.conn[self.db_name]
        self.collection = self.db['log']

    def tearDown(self):
        """ Drop used database """
        self.conn.drop_database(self.db_name)
        

    def testLogging(self):
        """ Simple logging example """
        log = logging.getLogger('')
        log.setLevel(logging.DEBUG)

        log.addHandler(MongoHandler(self.collection))
        log.debug('test')

        r = self.collection.find_one({'levelname':'DEBUG', 'msg':'test'})
        self.assertEquals(r['msg'], 'test')

    def testLoggingException(self):
        """ Logging example with exception """
        log = logging.getLogger('')
        log.setLevel(logging.DEBUG)

        log.addHandler(MongoHandler(self.collection))

        try:
            1/0
        except ZeroDivisionError:
            log.error('test zero division', exc_info=True)

        r = self.collection.find_one({'levelname':'ERROR', 'msg':'test zero division'})
        self.assertTrue(r['exc_info'].startswith('Traceback'))

    def testQueryableMessages(self):
        """ Logging example with dictionary """
        log = logging.getLogger('query')
        log.setLevel(logging.DEBUG)

        log.addHandler(MongoHandler(self.collection))

        log.info({'address': '340 N 12th St', 'state': 'PA', 'country': 'US'})
        log.info({'address': '340 S 12th St', 'state': 'PA', 'country': 'US'})
        log.info({'address': '1234 Market St', 'state': 'PA', 'country': 'US'})
    
        cursor = self.collection.find({'level':'info', 'msg.address': '340 N 12th St'})
        self.assertEquals(cursor.count(), 1, "Expected query to return 1 "
            "message; it returned %d" % cursor.count())
        self.assertEquals(cursor[0]['msg']['address'], '340 N 12th St')

        cursor = self.collection.find({'level':'info', 'msg.state': 'PA'})

        self.assertEquals(cursor.count(), 3, "Didn't find all three documents")
