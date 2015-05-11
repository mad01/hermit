#!/usr/bin/env python
import yaml
import sqlite3
from lib import sql
from lib import wsplit
from urlparse import urlparse
from flask import Flask, render_template, redirect, g, abort, request


app = Flask(__name__)
confFile = file('src/app.yml', 'r')
conf = yaml.load(confFile)
db = conf.get("app").get("db")
host = conf.get("app").get("host")
port = conf.get("app").get("port")
baseUrl = "http://" + host + "/"


def generate_random_short_url(url):
    """check if and of the words in the words in the url
    path is in the inactive table. If that is the case take
    the last matching one and use it to create a short url
    if not pick a random from the inactive table"""
    urlWordList = wsplit.url_split(url)
    shortWord = ""
    if urlWordList:
        for word in urlWordList:
            dbGet = sql.db_get_word_in_inactive(word, g.db)
            if dbGet and not shortWord:
                """if multiple words are found in inactive 
                the first selected word should be used
                and skip this since shortWord is true"""
                shortWord = dbGet.get("word")
                sql.db_remove_row_inactive(dbGet.get("id"), g.db)
    else:
        randWord = sql.db_get_random_word_from_inactive(g.db)
        sql.db_remove_row_inactive(randWord.get("id"), g.db)
        shortWord = randWord.get("word")

    shortUrl = baseUrl + shortWord
    sql.db_insert_row_active(
        g.db,
        url=url,
        word=shortWord
    )
    return shortUrl


@app.before_request
def before_request():
    """on request connect to the db"""
    g.db = sql.db_connect(db)


@app.teardown_request
def teardown_request(exception):
    """on request disconnect the db if connected"""
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    """index page with url shortner form. that retruns
    the shorted url"""
    if request.method == "POST":
        form_url = request.form['form_url']
        shortUrl = generate_random_short_url(form_url)
        return render_template("index.html", short_url=shortUrl)

    return render_template("index.html")


@app.route("/<short>", methods=["GET"])
def get_redirect(short):
    """retrun a redirect url using a input word"""
    redirect_url = sql.db_get_url_by_word(short, g.db)
    if redirect_url:
        return redirect(redirect_url.get("url"))
    else:
        abort(404)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=bool(conf.get('app').get('debug')),
        port=int(conf.get('app').get('port'))
    )
