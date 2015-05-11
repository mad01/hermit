#!/usr/bin/env python
import unittest
from scripts.db_word_import import word_file_clean


class TestWordClean(unittest.TestCase):

    def setUp(self):
        self.wordFile = 'tests/words.txt'

    def tearDown(self):
        pass

    def testClean(self):
        wordClean = word_file_clean(self.wordFile)
        for word in wordClean:
            self.assertEqual(word, 'abc123')


if __name__ == '__main__':
    unittest.main()
