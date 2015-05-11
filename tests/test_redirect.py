#!/usr/bin/env python
import unittest
import yaml
from requests import get

confFile = file('src/app.yml', 'r')
conf = yaml.load(confFile)
host = conf.get("app").get("host")
baseUrl = "http://" + host + "/"


class TestRedirect(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def TestRedirectValid_Google(self):
        word = "nathaniel"
        redirect_url = u'https://www.google.se/'
        res = get(baseUrl + word)
        self.assertEqual(res.url, redirect_url)
        self.assertEqual(res.status_code, 200)


    def TestRedirectValid_Facebook(self):
        word = "ordinary"
        redirect_url = u'https://www.facebook.com/'
        res = get(baseUrl + word)
        self.assertEqual(res.url, redirect_url)
        self.assertEqual(res.status_code, 200)


    def TestRedirectInValid(self):
        word = "foobar"
        res = get(baseUrl + word)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
