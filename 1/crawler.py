from bae.core import const
from bae.api import logging

import json
import tornado.web
import feedparser
import pymongo

BAIDU_SEARCH_URL = "http://www.baidu.com/baidu"

def crawl_news():
    logging.debug("crawler")
    logging.info("crawler")
    con = None
    try:
        ret = feedparser.parse("http://news.baidu.com/ns?word=%CE%DB%C8%BE&tn=newsrss&sr=0&cl=2&rn=20&ct=0") 

        db_name = 'ecomap'
        con = pymongo.Connection(host = const.MONGO_HOST, port = int(const.MONGO_PORT))
        db = con[db_name]

        logging.debug("const %s" % json.dumps(const))

        if const.MONGO_USER:
            db.authenticate(const.MONGO_USER, const.MONGO_PASS)
        news = db.news

        logging.debug("Found %d entries" % len(ret.entries))

        for entry in ret.entries:
            news.insert({
                "_id": entry.link,
                "title": entry.title,
                "description": entry.description
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
        crawl_news()

if __name__ == "__main__":
    crawl_news()