#!/usr/bin/env python
from urlparse import urlparse
import re


def url_split(url):
    """split url and return only strings in a list"""
    url_split = urlparse(url)
    url_path = url_split.path
    clean_url = re.sub('[^A-Za-z]+', ',', url_path).split(",")
    wordList = []
    for word in clean_url:
        """remove any empty strings and reverse back the list to the original
        order the strings are in the url"""
        if word:
            wordList.append(word)
    return wordList
