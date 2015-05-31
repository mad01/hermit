#!/usr/bin/env python
import sqlite3
from datetime import datetime


def db_connect(db):
    """Connect to the sqlite db"""
    return sqlite3.connect(db)


def db_get_url_by_word(word, db):
    """get the url for a word"""
    cursor = db.cursor()
    dbGet = cursor.execute("SELECT url FROM active WHERE word=?", (word,))
    dbRow = dbGet.fetchone()
    if dbRow:
        return {"url": dbRow[0]}
    else:
        return None


def db_get_word_in_inactive(word, db):
    """get the a word in inactive"""
    cursor = db.cursor()
    dbGet = cursor.execute("SELECT * FROM inactive WHERE word=?", (word,))
    dbRow = dbGet.fetchone()
    if dbRow:
        return {"word": str(dbRow[1]), "id": dbRow[0]}
    else:
        return None


def db_get_random_word_from_inactive(db):
    """get a random row using the random select function
    if no row is found get the oldest row in the active"""
    cursor = db.cursor()
    dbGet = cursor.execute("SELECT * FROM inactive ORDER BY RANDOM() LIMIT 1")
    dbRow = dbGet.fetchone()
    if dbRow:
        db_remove_row_inactive(dbRow[0], db)
        return {"word": str(dbRow[1])}
    if not dbRow:
        dbGetActive = db_get_oldest_row_in_active(db)
        return dbGetActive
    else:
        return None


def db_get_oldest_row_in_active(db):
    """get the oldest entry/row"""
    cursor = db.cursor()
    dbGet = cursor.execute("SELECT * FROM active ORDER BY ROWID ASC LIMIT 1")
    dbRow = dbGet.fetchone()
    if dbRow:
        dbDict = {"word": str(dbRow[2])}
        db_remove_row_active(dbRow[0], db)
        return dbDict
    else:
        return None


def db_remove_row_active(rowId, db):
    """remove a row with the id passed to the function in active"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM active WHERE id=?", (rowId,))
    db.commit()


def db_remove_row_active_by_word(word, db):
    """remove a row with the word passed to the function in active"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM active WHERE word=?", (word,))
    db.commit()


def db_remove_row_inactive(rowId, db):
    """remove a row the the id passed to the function in inactive"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM inactive WHERE id=?", (rowId,))
    db.commit()


def db_remove_word_inactive(word, db):
    """remove a row the the id passed to the function in inactive"""
    cursor = db.cursor()
    dbGet = cursor.execute("DELETE FROM inactive WHERE word=?", (word,))
    dbGet.fetchone()
    db.commit()


def db_remove_row_inactive_by_word(word, db):
    """remove a row with the word passed to the function in inactive"""
    cursor = db.cursor()
    cursor.execute("DELETE FROM inactive WHERE word=?", (word,))
    db.commit()


def db_insert_row_active(db, url="", word=""):
    """insert row with url and word"""
    now = datetime.now()
    cursor = db.cursor()
    cursor.execute("INSERT INTO active(id, url, word, created) VALUES (NULL,?,?,?)", (url.strip(), word, now,))
    db.commit()


def db_insert_row_inactive(db, word=""):
    """insert row with new word"""
    cursor = db.cursor()
    cursor.execute("INSERT INTO inactive(id, word) VALUES (NULL,?)", (word.strip(),))
    db.commit()
