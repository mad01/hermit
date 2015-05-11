#!/usr/bin/env python
import unittest
from src.lib import wsplit


class TestUrlWord(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_url_split(self):
        url = "http://example.com/foo345-/43/23-1/bar"
        words = ["foo", "bar"]
        clean_url = wsplit.url_split(url)
        self.assertEqual(words[0], clean_url[0])
        self.assertEqual(words[1], clean_url[1])


if __name__ == '__main__':
    unittest.main()
