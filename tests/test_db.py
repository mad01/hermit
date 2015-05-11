#!/usr/bin/env python
import unittest
import yaml
import sqlite3
from requests import get
from src.lib import sql


confFile = file('src/app.yml', 'r')
conf = yaml.load(confFile)
host = conf.get("app").get("host")
baseUrl = "http://" + host + "/"


class TestDb(unittest.TestCase):

    def setUp(self):
        """test setup creating a in memory sqlite db to be able to 
        start every test from a clean state. And to be able to 
        run any test in any order sinc every test should not be 
        dependent on a state created by some other test"""
        self.active = {"a": "https://www.google.com"}
        self.inactive = ["b", "c", "d", "e"]
        self.db = sqlite3.connect(':memory:')

        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE active(id INTEGER PRIMARY KEY,url TEXT,word TEXT,created DATETIME DEFAULT CURRENT_TIMESTAMP)")
        cursor.execute("CREATE TABLE inactive(id INTEGER PRIMARY KEY,word TEXT)")
        self.db.commit()

        sql.db_insert_row_active(
            self.db,
            url=self.active.get("a"),
            word="a"
        )
        for i in self.inactive:
            sql.db_insert_row_inactive(
                self.db,
                word=i
            )


    def tearDown(self):
        """close the db in memory to start next test in a clean state"""
        self.db.close()


    def test_db_get_url_by_word(self):
        word = "a"
        url = u"https://www.google.com"
        dbGet = sql.db_get_url_by_word(word, self.db)
        self.assertEqual(dbGet.get("url"), url)


    """not the best test needs some effort to do a random check
    that is a bit low prio atm. just testing that a word is 
    returned. NOTE this is ouside since nosetest uses a 
    doc string as a test name if there is one inside the test"""
    def test_db_get_random_word_from_inactive(self):
        dbGet = sql.db_get_random_word_from_inactive(self.db)
        self.assertIn(dbGet.get("word"), self.inactive)


    def test_db_that_if_inactive_empty_oldest_in_active_is_selected(self):
        for word in self.inactive:
            sql.db_remove_row_inactive_by_word(word, self.db)

        dbGet = sql.db_get_random_word_from_inactive(self.db)
        self.assertEqual(dbGet.get("word"), "a")


    def test_db_remove_row_active_by_word(self):
        sql.db_remove_row_active_by_word("a", self.db)
        dbGet = sql.db_get_url_by_word("a", self.db)
        self.assertIsNone(dbGet)


    def test_db_remove_row_inactive_by_word(self):
        sql.db_remove_word_inactive("b", self.db)
        dbGet = sql.db_get_word_in_inactive("b", self.db)
        self.assertIsNone(dbGet)


    def test_db_insert_row_active(self):
        test_url = "foo@example.com"
        test_word = "foo"
        sql.db_insert_row_active(
            self.db,
            url=test_url,
            word=test_word
        )
        dbGet = sql.db_get_url_by_word(test_word, self.db)
        self.assertEqual(dbGet.get("url"), unicode(test_url))


    def test_db_insert_row_active_check_whitespace_strip(self):
        test_url = " foo@example.com "
        test_word = "foo"
        sql.db_insert_row_active(
            self.db,
            url=test_url,
            word=test_word
        )
        dbGet = sql.db_get_url_by_word(test_word, self.db)
        self.assertEqual(dbGet.get("url"), unicode(test_url.strip()))


    def test_db_insert_row_inactive(self):
        test_word = "bar"
        sql.db_insert_row_inactive(self.db, word=test_word)
        dbGet = sql.db_get_word_in_inactive(test_word, self.db)
        self.assertEqual(dbGet.get("word"), test_word)


    def test_db_insert_row_inactive_check_whitespace_strip(self):
        test_word = " bar "
        sql.db_insert_row_inactive(self.db, word=test_word)
        dbGet = sql.db_get_word_in_inactive(test_word.strip(), self.db)
        self.assertEqual(dbGet.get("word"), test_word.strip())


    def test_db_get_oldest_row_in_active(self):
        sql.db_insert_row_active(
            self.db,
            url="foo@example.com",
            word="kaka"
        )
        dbGet = sql.db_get_oldest_row_in_active(self.db)
        self.assertEqual(dbGet.get("word"), "a")


if __name__ == '__main__':
    unittest.main()
