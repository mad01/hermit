#!/usr/bin/env python
import argparse
import re
import sqlite3


def word_file_clean(wordFile):
    word_file = open(wordFile, 'r').readlines()
    count = 0
    clean_word_dict = {}
    for word in word_file:
        """clean words of none alpha chars and change all to lower.
        using a dict to remove dupplications if there is any"""
        clean_word_dict.update(
            {
                count: str(re.sub('[^A-Za-z0-9]+', '', word)).lower()
            }
        )
        count += 1

    clean_word_list = []
    for num, word in clean_word_dict.iteritems():
        """change it back to a list of words"""
        clean_word_list.append(word)

    return clean_word_list


def db_word_import(wordList):
    """Insert all words in to the database and increment that
    primery key using the NULL value to the id"""
    db = sqlite3.connect('src/short.db')
    cursor = db.cursor()

    for word in wordList:
        cursor.execute("INSERT INTO inactive(id, word) VALUES (NULL,?)", (word,))

    db.commit()


if __name__ == "__main__":
    description = """
    clean word list file and add the words to sqlite.
    """
    parser = argparse.ArgumentParser(description)
    parser.add_argument('-f', '--file', help='input word file', required=True)
    args = parser.parse_args()

    cleaned = word_file_clean(args.file)
    db_word_import(cleaned)
