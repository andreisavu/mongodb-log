
import unittest
import logging

from pymongo.connection import Connection

from os.path import dirname
from logging.config import fileConfig, dictConfig

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
        
    def testLoggingFileConfiguration(self):
        log = logging.getLogger('example')
        log.debug('test')

        r = self.conn[self.db_name][self.collection_name]
    
        message = r.find_one({'level':'debug', 'msg':'test'})
        self.assertEquals(message['msg'], 'test')

class TestDictConfig(unittest.TestCase):
    def setUp(self):
        """ Create an empty database that could be used for logging """
        self.db_name = '_mongolog_test_dict'
        self.collection_name = 'log_test'

        self.configDict = {
            'version': 1,
            'handlers': {
                'mongo': {
                    'class': 'mongolog.handlers.MongoHandler',
                    'db': self.db_name,
                    'collection': self.collection_name,
                    'level': 'INFO'
                }
            },
            'root': {
                'handlers': ['mongo'],
                'level': 'INFO'
            }
        }

        self.conn = Connection('localhost')
        self.conn.drop_database(self.db_name)

    def testLoggingDictConfiguration(self):
        dictConfig(self.configDict)
        log = logging.getLogger('dict_example')
        log.debug('testing dictionary config')

        r = self.conn[self.db_name][self.collection_name]

        message = r.find_one({'level':'debug', 'msg':'dict_example'})
        self.assertEquals(message, None,
            "Logger put debug message in when info level handler requested")

        log.info('dict_example')
        message = r.find_one({'level':'info', 'msg':'dict_example'})
        self.assertNotEquals(message, None,
            "Logger didn't insert message into database")
        self.assertEquals(message['msg'], 'dict_example',
            "Logger didn't insert correct message into database")

    def tearDown(self):
        """ Drop used database """
        self.conn.drop_database(self.db_name)


