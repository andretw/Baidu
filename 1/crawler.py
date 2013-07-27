# -*- coding: utf-8 -*-

from bae.core import const
from bae.api import logging

import json
import tornado.web
import feedparser
import pymongo
from urllib import quote

from loc_keywords import locations

BAIDU_SEARCH_URL = "http://www.baidu.com/baidu"

def crawl_news(loc):
    logging.debug("crawler")
    logging.info("crawler")
    con = None
    try:
        loc_query = quote(loc.encode("gbk"))
        rss_url = "http://news.baidu.com/ns?word="+ loc_query +"%2B%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0"
        logging.debug("rss_url: " + rss_url)
        ret = feedparser.parse(rss_url) 

        db_name = 'ZwgmbiQSlqOsjZWOKIOJ'
        con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
        db = con[db_name]

        if const.MONGO_USER:
            db.authenticate(const.MONGO_USER, const.MONGO_PASS)
        news = db.news

        logging.debug("Found %d entries" % len(ret.entries))

        for entry in ret.entries:
            news.insert({
                "_id": entry.link,
                "title": entry.title,
                "description": entry.description,
                "loc": loc
            })
    except:
        logging.exception('ERROR when crawl')
    finally:
        if con:
            con.disconnect()

class CrawlerHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        for loc in locations:
            crawl_news(loc)

if __name__ == "__main__":
    crawl_news(u"北京")